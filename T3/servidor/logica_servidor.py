from funciones import valor_parametro, SalaEspera, Juego, Jugador


class LogicaServidor:

    def __init__(self, parent):
        self.parent = parent
        self.usuarios = {}
        self.sala_espera = SalaEspera()
        self.juego = None

    def procesar_mensaje(self, mensaje: dict, id):
        try:
            asunto = mensaje["asunto"]
        except KeyError:
            return {}

        if asunto == "validar usuario":
            valido, error = self.validar_usuario(mensaje["usuario"], id)
            return {
                "asunto": "respuesta validacion usuario",
                "valido": valido,
                "error": error
            }

        elif asunto == "ingresar sala espera":
            respuesta = {
                "asunto": "respuesta ingresar sala espera",
                "ingresar": False,
                "oponente": None,
                "id": id,
            }
            if self.sala_espera.capacidad:
                respuesta["ingresar"] = True
                self.usuarios[id] = mensaje["usuario"].lower()
                self.parent.log(self.usuarios[id], "Ingreso sala espera", "Aceptado")
                self.sala_espera.agregar_jugador(id)
                if len(self.sala_espera.jugadores) == 2:
                    id_oponente = self.sala_espera.jugadores[0]
                    self.crear_partida(id, id_oponente)
                    oponente = self.usuarios[id_oponente]
                    respuesta["oponente"] = oponente
                    self.parent.log(f"{self.usuarios[id]}, {oponente}", "Conectando jugadores", "-")
            else:
                if self.sala_espera.juego_en_curso:
                    self.parent.log(mensaje["usuario"], "Ingreso sala espera",
                                    "Rechazado. Juego en curso")
                    respuesta["error"] = "juego en curso"
                else:
                    self.parent.log(mensaje["usuario"], "Ingreso sala espera",
                                    "Rechazado. Sin capacidad")
                    respuesta["error"] = "sin capacidad"
            return respuesta

        elif asunto == "salir sala espera":
            self.sala_espera.desconectar_jugador(id)
            self.usuarios.pop(id, None)

        elif asunto == "actualizar ventana":
            respuesta = {
                "asunto": "actualizacion ventana",
                "estado": mensaje["estado"]
            }
            # Actualizar ventana sala espera
            if mensaje["estado"] == "sala espera":
                if not self.sala_espera.capacidad:  # Cuando se llena comienza tiempo
                    respuesta["segundos"] = self.sala_espera.cuenta_regresiva.segundos
                    for id_jugador in self.sala_espera.jugadores:
                        if id_jugador != id:
                            respuesta["oponente"] = self.usuarios[id_jugador]
                else:
                    respuesta["segundos"] = self.sala_espera.segundos
                    respuesta["oponente"] = None

            # Actualizar ventana juego
            elif mensaje["estado"] == "ronda":
                if self.juego:
                    if self.juego.ganador_juego is None:
                        respuesta["ganador juego"] = None

                        # Segundos
                        if self.juego.tiempo_corriendo_ronda:
                            respuesta["segundos"] = self.juego.tiempo_ronda.segundos
                        elif self.juego.tiempo_corriendo_pausa:
                            respuesta["segundos"] = self.juego.tiempo_pausa.segundos
                        else:
                            respuesta["segundos"] = self.juego.segundos_ronda

                        # Actualizacion juego
                        if id == self.juego.jugador_1.id:  # Para que entre una vez
                            if self.juego.iniciando_partida:
                                self.sala_espera.juego_en_curso = True
                                usuario_1 = self.juego.jugador_1.usuario
                                usuario_2 = self.juego.jugador_2.usuario
                                self.parent.log(
                                    f"{usuario_1}, {usuario_2}", "Iniciando partida", "-")
                            for id_jugador in self.juego.jugadores:
                                jugador = self.juego.jugadores[id_jugador]
                                if self.juego.tiempo_corriendo_ronda:
                                    segundos = self.juego.tiempo_ronda.segundos
                                    if segundos == 0 and jugador.carta_seleccionada is None:
                                        self.parent.log(jugador.usuario, "Tiempo acabado",
                                                        "Jugara carta al azar")
                            self.juego.actualizar()

                        # Info
                        respuesta["ronda actual"] = self.juego.ronda_actual
                        respuesta["regresar ronda"] = self.juego.regresar_ronda
                        respuesta["ganador"] = None
                        if self.juego.ronda_terminada:
                            ganador = self.juego.resultado_ronda[0]
                            respuesta["gano partida"] = self.juego.resultado_ronda[1]
                            cartas_jugadores = self.juego.resultado_ronda[2]
                            for id_jugador in cartas_jugadores:
                                if id_jugador != id:
                                    carta_oponente = cartas_jugadores[id_jugador]
                            respuesta["carta oponente"] = carta_oponente
                            respuesta["carta jugador"] = cartas_jugadores[id]
                            if ganador == id:
                                respuesta["ganador"] = "jugador"
                                usuario_ganador = self.usuarios[id]
                            else:
                                if ganador != "empate":
                                    respuesta["ganador"] = "oponente"
                                    usuario_ganador = self.usuarios[id_jugador]
                                else:
                                    respuesta["ganador"] = "empate"
                            if id == self.juego.jugador_1.id and not self.juego.ronda_revisada:
                                self.juego.ronda_revisada = True
                                n = self.juego.ronda_actual
                                if ganador != "empate":
                                    self.parent.log("-", f"Ronda {n} terminada",
                                                    f"Ganador: {usuario_ganador}")
                                else:
                                    self.parent.log("-", f"Ronda {n} terminada", "Empate")
                                if respuesta["gano partida"]:
                                    self.sala_espera.liberar()
                                    self.parent.log("-", "Juego terminado",
                                                    f"Ganador: {usuario_ganador}")
                                    self.parent.log("-", "Sala espera liberada", "-")
                    else:
                        self.sala_espera.liberar()
                        respuesta["ganador juego"] = True
                        self.parent.log("-", "Juego terminado", f"Ganador: {self.usuarios[id]}")
                        self.parent.log("-", "Sala espera liberada", "-")
            return respuesta

        elif asunto == "carta bandeja":
            jugador = self.juego.jugadores[id]
            posicion = mensaje["posicion"]
            carta = jugador.cartas_bandeja[posicion]
            return {
                "asunto": "reponer carta",
                "carta": carta,
                "posicion": posicion
            }

        elif asunto == "carta elegida":
            jugador = self.juego.jugadores[id]
            tipo_carta = jugador.tipo_carta(mensaje["numero"])
            self.parent.log(self.usuarios[id], "Carta elegida", f"Carta tipo {tipo_carta}")
            nueva_carta_bandeja = self.juego.seleccionar_carta(id, mensaje["numero"])
            self.juego.revisar_terminar_ronda()
            return {
                "asunto": "reponer carta",
                "carta": nueva_carta_bandeja,
                "posicion": mensaje["numero"]
            }

        elif asunto == "utilizar boton bienestar":
            jugador = self.juego.jugadores[id]
            usar_boton = self.juego.usar_boton_bienestar(jugador)
            if usar_boton:
                self.parent.log(self.usuarios[id], "Usar boton bienestar", "Aceptado")
            else:
                self.parent.log(self.usuarios[id], "Usar boton bienestar", "Rechazado")
            return {
                "asunto": "respuesta boton bienestar",
                "usar": usar_boton
            }

        elif asunto == "guardar tecla":
            carta_oponente = None
            ver_carta_oponente = self.juego.jugadores[id].ver_oponente(mensaje["tecla"])
            if ver_carta_oponente:
                for id_jugador in self.juego.jugadores:
                    if id_jugador != id:
                        oponente = self.juego.jugadores[id_jugador]
                        if oponente.carta_seleccionada is not None:
                            carta_oponente = oponente.carta_seleccionada
                            self.parent.log(self.usuarios[id], "Viendo carta oponente", "-")
                return {
                    "asunto": "ver carta oponente",
                    "carta": carta_oponente
                }

        elif asunto == "terminar jugada":
            if self.juego:
                for id_jugador in self.juego.jugadores:
                    self.usuarios.pop(id_jugador, None)
            self.juego = None

    def validar_usuario(self, usuario, id):
        rango_usuario = valor_parametro("RANGO_USUARIO")
        if (usuario.isdigit()):
            self.parent.log(usuario, "Validación usuario", "Inválido")
            return False, "alfanumerico"
        else:
            if len(usuario) >= rango_usuario[0] and len(usuario) <= rango_usuario[1]:
                # Revisar si existe
                if usuario in list(self.usuarios.values()):
                    self.parent.log(usuario, "Validación usuario", "Inválido")
                    return False, "existe"
                else:
                    self.parent.log(usuario, "Validación usuario", "Válido")
                    return True, ""
            else:
                self.parent.log(usuario, "Validación usuario", "Inválido")
                return False, "rango"

    def eliminar_jugador(self, id):
        self.usuarios.pop(id, None)
        # Desconectar de sala de espera
        if id in self.sala_espera.jugadores:
            self.sala_espera.desconectar_jugador(id)
        # Desconectar partida
        if self.juego is not None:
            jugador_en_partida = False
            for id_jugador in self.juego.jugadores:
                if id_jugador == id:
                    jugador_en_partida = True
            if jugador_en_partida:
                for id_jugador in self.juego.jugadores:
                    if id_jugador != id:
                        self.juego.ganador_juego = self.juego.jugadores[id_jugador]

    def crear_partida(self, id_jugador_1, id_jugador_2):
        usuario_jugador_1 = self.usuarios[id_jugador_1]
        usuario_jugador_2 = self.usuarios[id_jugador_2]
        jugador_1 = Jugador(id_jugador_1, usuario_jugador_1)
        jugador_2 = Jugador(id_jugador_2, usuario_jugador_2)
        self.juego = Juego(jugador_1, jugador_2)
