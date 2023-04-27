import json
import os.path
from time import sleep
from random import choice
from PyQt5.QtCore import QObject, QThread
from scripts.cartas import get_penguins


def valor_parametro(llave):
    ruta = os.path.join("parametros.json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        diccionario = json.load(archivo)
    valor = diccionario[llave]
    return valor


class SalaEspera(QObject):
    def __init__(self):
        super().__init__()
        self.segundos = valor_parametro("CUENTA_REGRESIVA_INICIO")
        self.capacidad = True
        self.juego_en_curso = False
        self.jugadores = []

    def iniciar_timer(self):
        self.cuenta_regresiva = CuentaRegresiva(self.segundos)
        self.cuenta_regresiva.start()

    def agregar_jugador(self, id_jugador):
        self.jugadores.append(id_jugador)
        if len(self.jugadores) == 2:
            self.capacidad = False
            self.iniciar_timer()

    def desconectar_jugador(self, id_jugador):
        self.jugadores.pop(self.jugadores.index(id_jugador))
        self.capacidad = True
        self.juego_en_curso = False

    def liberar(self):
        self.capacidad = True
        self.juego_en_curso = False
        self.jugadores.clear()


class Juego(QObject):
    def __init__(self, jugador_1, jugador_2):
        super().__init__()
        self.jugador_1 = jugador_1
        self.jugador_2 = jugador_2
        self.jugadores = {
            jugador_1.id: jugador_1,
            jugador_2.id: jugador_2
        }
        self.ronda_actual = 0
        self.segundos_ronda = valor_parametro("CUENTA_REGRESIVA_RONDA")
        self.segundos_pausa = valor_parametro("CUENTA_REGRESIVA_REGRESAR_RONDA")
        self.regresar_ronda = False
        self.ronda_terminada = False
        self.ronda_revisada = False
        self.partida_terminada = False
        self.ganador_ronda = None
        self.ganador_juego = None
        self.resultado_ronda = [None, None, None]  # Id ganador, gano partida, cartas jugadores
        self.iniciando_partida = True
        self.tiempo_corriendo_ronda = False
        self.tiempo_corriendo_pausa = False

    def iniciar_tiempo_ronda(self):
        self.ronda_actual += 1
        self.ronda_revisada = False
        self.ronda_terminada = False
        self.tiempo_corriendo_ronda = True
        self.resultado_ronda = [None, None, None]
        self.tiempo_ronda = CuentaRegresiva(self.segundos_ronda)
        self.tiempo_ronda.start()

    def iniciar_tiempo_pausa(self):
        self.tiempo_corriendo_pausa = True
        self.tiempo_pausa = CuentaRegresiva(self.segundos_pausa)
        self.tiempo_pausa.start()

    def actualizar(self):
        if self.iniciando_partida:
            self.iniciando_partida = False
            self.iniciar_tiempo_ronda()

        if self.tiempo_corriendo_ronda:
            if self.tiempo_ronda.segundos == 0 and not self.ronda_terminada:
                self.tiempo_corriendo_ronda = False

                self.resultado_ronda = self.definir_ganador_ronda()
                self.ronda_terminada = True
                self.iniciar_tiempo_pausa()

        if self.tiempo_corriendo_pausa:
            self.regresar_ronda = False
            if self.tiempo_pausa.segundos == 0:
                self.tiempo_corriendo_pausa = False
                self.regresar_ronda = True
                if not self.partida_terminada:
                    self.iniciar_tiempo_ronda()

    def seleccionar_carta(self, id, numero):
        jugador = self.jugadores[id]
        nueva_carta_bandeja = jugador.seleccionar_carta(numero)
        return nueva_carta_bandeja

    def revisar_terminar_ronda(self):
        if self.jugador_1.carta_seleccionada and self.jugador_2.carta_seleccionada:
            self.tiempo_corriendo_ronda = False
            self.ronda_terminada = True
            self.resultado_ronda = self.definir_ganador_ronda()
            self.iniciar_tiempo_pausa()

    def definir_ganador_ronda(self):
        carta_jugador_1 = self.jugador_1.carta_seleccionada
        carta_jugador_2 = self.jugador_2.carta_seleccionada
        if carta_jugador_1 is None:
            carta_jugador_1 = self.jugador_1.sacar_al_azar()
        if carta_jugador_2 is None:
            carta_jugador_2 = self.jugador_2.sacar_al_azar()

        if carta_jugador_1["elemento"] != carta_jugador_2["elemento"]:
            if carta_jugador_1["elemento"] == "fuego":
                if carta_jugador_2["elemento"] == "nieve":
                    ganador = "jugador 1"
                elif carta_jugador_2["elemento"] == "agua":
                    ganador = "jugador 2"
            elif carta_jugador_1["elemento"] == "nieve":
                if carta_jugador_2["elemento"] == "fuego":
                    ganador = "jugador 2"
                elif carta_jugador_2["elemento"] == "agua":
                    ganador = "jugador 1"
            elif carta_jugador_1["elemento"] == "agua":
                if carta_jugador_2["elemento"] == "fuego":
                    ganador = "jugador 1"
                elif carta_jugador_2["elemento"] == "nieve":
                    ganador = "jugador 2"
        else:
            if carta_jugador_1["puntos"] > carta_jugador_2["puntos"]:
                ganador = "jugador 1"
            elif carta_jugador_1["puntos"] < carta_jugador_2["puntos"]:
                ganador = "jugador 2"
            else:
                ganador = "empate"

        cartas_jugadores = {
            self.jugador_1.id: carta_jugador_1,
            self.jugador_2.id: carta_jugador_2
        }
        self.jugador_1.deseleccionar_carta()
        self.jugador_2.deseleccionar_carta()
        if ganador == "jugador 1":
            self.jugador_2.cartas_baraja.append(carta_jugador_2)
            fichas = self.jugador_1.fichas
            fichas.append(carta_jugador_1)
            gano_partida = self.revisar_fichas(fichas)
            return [self.jugador_1.id, gano_partida, cartas_jugadores]
        elif ganador == "jugador 2":
            self.jugador_1.cartas_baraja.append(carta_jugador_1)
            fichas = self.jugador_2.fichas
            fichas.append(carta_jugador_2)
            gano_partida = self.revisar_fichas(fichas)
            return [self.jugador_2.id, gano_partida, cartas_jugadores]
        elif ganador == "empate":
            self.jugador_1.cartas_baraja.append(carta_jugador_1)
            self.jugador_2.cartas_baraja.append(carta_jugador_2)
            return ["empate", False, cartas_jugadores]

    def revisar_fichas(self, fichas):
        gano = False
        colores = {}
        for carta in fichas:
            if carta["color"] not in colores:
                colores[carta["color"]] = [carta["elemento"]]
            else:
                if carta["elemento"] not in colores[carta["color"]]:
                    colores[carta["color"]].append(carta["elemento"])
        if len(colores) == 3:
            # Revisar elementos distintos
            for i in range(len(colores["azul"])):
                elementos = []
                elementos.append(colores["azul"][i])
                for j in range(len(colores["verde"])):
                    elemento = colores["verde"][j]
                    if elemento not in elementos:
                        elementos.append(elemento)
                        for n in range(len(colores["rojo"])):
                            elemento = colores["rojo"][n]
                            if elemento not in elementos:
                                elementos.append(elemento)
                                gano = True
                                self.partida_terminada = True
            # Revisar elementos iguales
            cantidad_agua = 0
            cantidad_fuego = 0
            cantidad_nieve = 0
            for color in colores:
                if "agua" in colores[color]:
                    cantidad_agua += 1
                if "fuego" in colores[color]:
                    cantidad_fuego += 1
                if "nieve" in colores[color]:
                    cantidad_nieve += 1
            if cantidad_agua == 3 or cantidad_fuego == 3 or cantidad_nieve == 3:
                gano = True
                self.partida_terminada = True
        return gano

    def usar_boton_bienestar(self, jugador):
        fichas = jugador.fichas
        colores = {}
        for carta in fichas:
            if carta["color"] not in colores:
                colores[carta["color"]] = [carta["elemento"]]
            else:
                if carta["elemento"] not in colores[carta["color"]]:
                    colores[carta["color"]].append(carta["elemento"])
        if not jugador.boton_bienestar:
            if len(colores) == 3:
                self.ganador_ronda = jugador
                jugador.boton_bienestar = True
                for id in self.jugadores:
                    if id != self.ganador_ronda.id:
                        id_oponente = id
                cartas_jugadores = {
                    self.ganador_ronda.id: self.ganador_ronda.sacar_al_azar(),
                    id_oponente: None
                }
                gano = self.revisar_fichas(self.ganador_ronda.fichas)
                self.resultado_ronda = [self.ganador_ronda.id, gano, cartas_jugadores]
                self.ronda_terminada = True
                self.tiempo_corriendo_ronda = False
                self.iniciar_tiempo_pausa()
                return True
            else:
                return False
        else:
            return False


class Jugador:
    def __init__(self, id, usuario):
        self.id = id
        self.usuario = usuario
        self.cartas_baraja = get_penguins()
        self.fichas = []
        self.carta_seleccionada = None
        self.cartas_bandeja = {}
        self.boton_bienestar = False
        self.teclas = "   "
        self.preparar_cartas()

    def preparar_cartas(self):
        lista_cartas = []
        for i in range(15):
            lista_cartas.append(self.cartas_baraja[str(i)])
        self.cartas_baraja = lista_cartas
        for i in range(valor_parametro("CARTAS_BANDEJA")):
            self.cartas_bandeja[i + 1] = self.cartas_baraja.pop()

    def tipo_carta(self, numero_bandeja):
        carta = self.cartas_bandeja[numero_bandeja]
        tipo = carta["elemento"]
        return tipo

    def seleccionar_carta(self, numero_bandeja):
        self.carta_seleccionada = self.cartas_bandeja[numero_bandeja]
        self.cartas_bandeja.pop(numero_bandeja)
        # Reponer bandeja
        if self.cartas_baraja:
            nueva_carta_bandeja = self.cartas_baraja.pop(0)
            self.cartas_bandeja[numero_bandeja] = nueva_carta_bandeja
            return nueva_carta_bandeja
        else:
            return None

    def deseleccionar_carta(self):
        self.carta_seleccionada = None

    def sacar_al_azar(self):
        if self.cartas_baraja:
            carta = choice(self.cartas_baraja)
            return carta

    def ver_oponente(self, tecla):
        self.teclas += tecla
        if self.teclas[-3:] == "veo":
            return True
        else:
            return False


class CuentaRegresiva(QThread):
    def __init__(self, segundos):
        super().__init__()
        self.segundos = segundos

    def run(self):
        cuenta_regresiva = self.segundos
        for _ in range(cuenta_regresiva):
            sleep(1)
            self.segundos -= 1
