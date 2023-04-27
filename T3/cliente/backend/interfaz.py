from PyQt5.QtCore import QObject, pyqtSignal
from funciones import seleccionar_ruta_carta, seleccionar_ruta_ficha
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_espera import VentanaEspera
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_final import VentanaFinal


class Interfaz(QObject):
    """
    Usuario recibe e interpreta mensajes del servidor.
    """
    senal_respuesta_validacion = pyqtSignal(bool, str)
    senal_respuesta_ingreso_sala_espera = pyqtSignal(bool, str)
    senal_oponente_conectado = pyqtSignal(str)
    senal_oponente_desconectado = pyqtSignal()
    senal_actualizar_segundos_sala_espera = pyqtSignal(int)
    senal_actualizar_segundos_ronda = pyqtSignal(int)
    senal_actualizar_ronda_actual = pyqtSignal(int)
    senal_actualizar_carta = pyqtSignal(str, int, str)
    senal_agregar_ficha = pyqtSignal(str, str)
    senal_mostrar_ganador_ronda = pyqtSignal(str, bool, str, str)
    senal_regresar_ronda = pyqtSignal()
    senal_respuesta_boton_bienestar = pyqtSignal(bool)
    senal_mostrar_carta_oponente = pyqtSignal(str)
    senal_ganador_juego = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()
        self.ventana_final = VentanaFinal()
        self.oponente_conectado = False
        self.ganador_anunciado = False
        self.ronda_preparada = False

    def operar_mensaje(self, mensaje: dict):
        try:
            asunto = mensaje["asunto"]

            if asunto == "respuesta validacion usuario":
                self.senal_respuesta_validacion.emit(mensaje["valido"], mensaje["error"])

            elif asunto == "respuesta ingresar sala espera":
                if mensaje["ingresar"]:
                    if mensaje["oponente"]:
                        usuario_oponente = mensaje["oponente"]
                        self.senal_oponente_conectado.emit(usuario_oponente)
                    self.senal_respuesta_ingreso_sala_espera.emit(True, "")
                else:
                    error = mensaje["error"]
                    self.senal_respuesta_ingreso_sala_espera.emit(False, error)

            elif asunto == "actualizacion ventana":
                estado = mensaje["estado"]
                if estado == "sala espera":
                    segundos = mensaje["segundos"]
                    self.senal_actualizar_segundos_sala_espera.emit(segundos)
                    if segundos == 0:
                        self.ventana_espera.esconder_ventana()
                    if mensaje["oponente"] and not self.oponente_conectado:
                        self.oponente_conectado = True
                        self.oponente = mensaje["oponente"]
                        self.senal_oponente_conectado.emit(self.oponente)
                    elif not mensaje["oponente"] and self.oponente_conectado:
                        self.oponente_conectado = False
                        self.senal_oponente_desconectado.emit()
                elif estado == "ronda":
                    if mensaje["ganador juego"] is None:
                        segundos = mensaje["segundos"]
                        self.senal_actualizar_segundos_ronda.emit(segundos)
                        ronda_actual = mensaje["ronda actual"]
                        self.senal_actualizar_ronda_actual.emit(ronda_actual)
                        if mensaje["ganador"] is not None and not self.ganador_anunciado:
                            self.ganador_anunciado = True
                            ganador = mensaje["ganador"]
                            carta_jugador = mensaje["carta jugador"]
                            carta_oponente = mensaje["carta oponente"]
                            ruta_carta_jugador = seleccionar_ruta_carta(carta_jugador)
                            ruta_carta_oponente = seleccionar_ruta_carta(carta_oponente)
                            gano_partida = mensaje["gano partida"]
                            if gano_partida:
                                self.ronda_preparada = False
                                self.ganador_anunciado = False
                            self.senal_mostrar_ganador_ronda.emit(
                                ganador, gano_partida, ruta_carta_jugador, ruta_carta_oponente)
                            if ganador != "empate":
                                if ganador == "jugador":
                                    ruta_ficha = seleccionar_ruta_ficha(carta_jugador)
                                elif ganador == "oponente":
                                    ruta_ficha = seleccionar_ruta_ficha(carta_oponente)
                                self.senal_agregar_ficha.emit(ganador, ruta_ficha)
                        if mensaje["regresar ronda"] and not self.ronda_preparada:
                            self.ronda_preparada = True
                            self.ganador_anunciado = False
                            self.senal_regresar_ronda.emit()
                        elif not mensaje["regresar ronda"]:
                            self.ronda_preparada = False
                    else:
                        self.senal_ganador_juego.emit()

            elif asunto == "respuesta boton bienestar":
                self.senal_respuesta_boton_bienestar.emit(mensaje["usar"])

            elif asunto == "reponer carta":
                carta = mensaje["carta"]
                posicion = mensaje["posicion"]
                if carta is not None:
                    ruta = seleccionar_ruta_carta(carta)
                else:
                    ruta = ""
                self.senal_actualizar_carta.emit("bandeja", posicion, ruta)

            elif asunto == "ver carta oponente":
                ruta = seleccionar_ruta_carta(mensaje["carta"])
                self.senal_mostrar_carta_oponente.emit(ruta)

        except KeyError:
            print("Asunto no encontrado en mensaje.")
            return {}
