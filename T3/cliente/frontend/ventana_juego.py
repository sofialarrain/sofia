from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel
import os.path
from funciones import valor_parametro

ruta = os.path.join(*valor_parametro("RUTA_VENTANA_JUEGO"))

window_name, base_class = uic.loadUiType(ruta)


class VentanaJuego(window_name, base_class):

    senal_carta_bandeja = pyqtSignal(dict)
    senal_carta_elegida = pyqtSignal(dict)
    senal_actualizar_ventana = pyqtSignal(dict)
    senal_mostrar_ventana_final = pyqtSignal(str)
    senal_boton_bienestar = pyqtSignal(dict)
    senal_tecla = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()
        self.fichas = []
        self.turno_fichas_oponente = 1
        self.turno_fichas_jugador = 1
        self.carta_seleccionada = None
        self.rutas_cartas_bandeja = {}
        self.ruta_carta_back = os.path.join(*valor_parametro("RUTA_BACK"))
        self.definir_posiciones_fichas()
        self.configurar_timer()

    def init_gui(self):
        self.carta_1.clicked.connect(self.seleccionar_carta_1)
        self.carta_2.clicked.connect(self.seleccionar_carta_2)
        self.carta_3.clicked.connect(self.seleccionar_carta_3)
        self.carta_4.clicked.connect(self.seleccionar_carta_4)
        self.carta_5.clicked.connect(self.seleccionar_carta_5)
        self.boton_seleccionar.clicked.connect(self.carta_elegida)
        self.boton_bienestar.clicked.connect(self.usar_boton_bienestar)

    def definir_posiciones_fichas(self):
        self.posicion_fichas_oponente_1 = valor_parametro("POSICION_FICHAS_OPONENTE_1")
        self.posicion_fichas_oponente_2 = valor_parametro("POSICION_FICHAS_OPONENTE_2")
        self.posicion_fichas_jugador_1 = valor_parametro("POSICION_FICHAS_JUGADOR_1")
        self.posicion_fichas_jugador_2 = valor_parametro("POSICION_FICHAS_JUGADOR_2")
        self.dimension_ficha = valor_parametro("DIMENSION_FICHA")

    def configurar_timer(self):
        # Timer actualización ventana
        self.timer_actualizar_ventana = QTimer()
        self.timer_actualizar_ventana.setInterval(valor_parametro("INTERVALO_ACTUALIZAR_VENTANA"))
        self.timer_actualizar_ventana.timeout.connect(self.actualizar_ventana)

    def mostrar_ventana(self, jugador, oponente):
        self.resetear_ventana()
        self.usuario_jugador.setText(jugador)
        self.usuario_oponente.setText(oponente)
        self.actualizar_tiempo(valor_parametro("CUENTA_REGRESIVA_RONDA"))
        self.timer_actualizar_ventana.start()
        self.preparar_ronda()
        for i in range(1, 6):
            self.senal_carta_bandeja.emit({
                "asunto": "carta bandeja",
                "posicion": i
            })
        self.show()

    def preparar_ronda(self):
        pixeles_carta_back = QPixmap(self.ruta_carta_back)
        transparente = """font: 75 20pt "Segoe UI Variable Display Semib";
                        color: rgb(255, 255, 255);
                        border-radius: 10px;
                        background-color: rgba(255, 255, 255, 0);"""
        self.carta_1.setEnabled(True)
        self.carta_2.setEnabled(True)
        self.carta_3.setEnabled(True)
        self.carta_4.setEnabled(True)
        self.carta_5.setEnabled(True)
        self.boton_seleccionar.setEnabled(False)
        self.mensaje_boton.hide()
        self.label_jugador.setStyleSheet(transparente)
        self.label_oponente.setStyleSheet(transparente)
        self.carta_jugador.setPixmap(pixeles_carta_back)
        self.carta_jugador.setScaledContents(True)
        self.carta_oponente.setPixmap(pixeles_carta_back)
        self.carta_oponente.setScaledContents(True)
        self.empate.hide()

    def actualizar_ventana(self):
        self.senal_actualizar_ventana.emit({
            "asunto": "actualizar ventana",
            "estado": "ronda",
        })

    def actualizar_carta(self, tipo, numero, ruta):
        if ruta != "":
            if tipo == "bandeja":
                self.rutas_cartas_bandeja[numero] = ruta
                if numero == 1:
                    self.carta_1.setIcon(QIcon(ruta))
                elif numero == 2:
                    self.carta_2.setIcon(QIcon(ruta))
                elif numero == 3:
                    self.carta_3.setIcon(QIcon(ruta))
                elif numero == 4:
                    self.carta_4.setIcon(QIcon(ruta))
                elif numero == 5:
                    self.carta_5.setIcon(QIcon(ruta))
            elif tipo == "elegida":
                pixeles = QPixmap(ruta)
                if numero == 1:
                    self.carta_oponente.setPixmap(pixeles)
                    self.carta_oponente.setScaledContents(True)
                elif numero == 2:
                    self.carta_jugador.setPixmap(pixeles)
                    self.carta_jugador.setScaledContents(True)
        else:
            if numero == 1:
                self.carta_1.clear()
            elif numero == 2:
                self.carta_2.clear()
            elif numero == 3:
                self.carta_3.clear()
            elif numero == 4:
                self.carta_4.clear()
            elif numero == 5:
                self.carta_5.clear()

    def actualizar_tiempo(self, segundo):
        self.segundos.setText(str(segundo))

    def actualizar_ronda_actual(self, ronda_actual):
        self.ronda_actual.setText(str(ronda_actual))

    def seleccionar_carta_1(self):
        self.carta_seleccionada = 1
        self.boton_seleccionar.setEnabled(True)

    def seleccionar_carta_2(self):
        self.carta_seleccionada = 2
        self.boton_seleccionar.setEnabled(True)

    def seleccionar_carta_3(self):
        self.carta_seleccionada = 3
        self.boton_seleccionar.setEnabled(True)

    def seleccionar_carta_4(self):
        self.carta_seleccionada = 4
        self.boton_seleccionar.setEnabled(True)

    def seleccionar_carta_5(self):
        self.carta_seleccionada = 5
        self.boton_seleccionar.setEnabled(True)

    def carta_elegida(self):
        ruta = self.rutas_cartas_bandeja[self.carta_seleccionada]
        pixeles = QPixmap(ruta)
        self.carta_jugador.setPixmap(pixeles)
        self.carta_jugador.setScaledContents(True)
        self.carta_1.setEnabled(False)
        self.carta_2.setEnabled(False)
        self.carta_3.setEnabled(False)
        self.carta_4.setEnabled(False)
        self.carta_5.setEnabled(False)
        self.boton_seleccionar.setEnabled(False)
        self.senal_carta_elegida.emit({
            "asunto": "carta elegida",
            "numero": self.carta_seleccionada
        })

    def mostrar_ganador_ronda(self, ganador, gano_partida, ruta_carta_jugador, ruta_carta_oponente):
        self.carta_1.setEnabled(False)
        self.carta_2.setEnabled(False)
        self.carta_3.setEnabled(False)
        self.carta_4.setEnabled(False)
        self.carta_5.setEnabled(False)
        self.boton_seleccionar.setEnabled(False)
        if ruta_carta_oponente is not None and ruta_carta_oponente != "":
            pixeles = QPixmap(ruta_carta_oponente)
            self.carta_oponente.setPixmap(pixeles)
            self.carta_oponente.setScaledContents(True)
        else:
            pixeles = QPixmap(self.ruta_carta_back)
            self.carta_oponente.setPixmap(pixeles)
            self.carta_oponente.setScaledContents(True)
        verde = """font: 75 20pt "Segoe UI Variable Display Semib";
                color: rgb(255, 255, 255);
                border-radius: 10px;
                background-color: rgba(0, 207, 0, 180);"""
        rojo = """font: 75 20pt "Segoe UI Variable Display Semib";
                color: rgb(255, 255, 255);
                border-radius: 10px;
                background-color: rgba(238, 0, 0, 180);"""
        amarillo = """font: 75 20pt "Segoe UI Variable Display Semib";
                color: rgb(255, 255, 255);
                border-radius: 10px;
                background-color: rgba(227, 227, 0, 180);"""
        if not gano_partida:
            if ganador == "oponente":
                self.label_oponente.setStyleSheet(verde)
                self.label_jugador.setStyleSheet(rojo)
            elif ganador == "jugador":
                self.label_jugador.setStyleSheet(verde)
                self.label_oponente.setStyleSheet(rojo)
            elif ganador == "empate":
                self.label_jugador.setStyleSheet(amarillo)
                self.label_oponente.setStyleSheet(amarillo)
                self.empate.show()
        else:
            self.hide()
            self.resetear_ventana()
            self.timer_actualizar_ventana.stop()
            self.senal_mostrar_ventana_final.emit(ganador)
        if ruta_carta_jugador is not None and ruta_carta_jugador != "":
            pixeles = QPixmap(ruta_carta_jugador)
            self.carta_jugador.setPixmap(pixeles)
            self.carta_jugador.setScaledContents(True)
        self.carta_seleccionada = None

    def agregar_ficha(self, jugador, ruta):
        ancho = self.dimension_ficha[0]
        alto = self.dimension_ficha[1]
        if jugador == "jugador":
            if self.turno_fichas_jugador == 1:
                x = self.posicion_fichas_jugador_1[0]
                y = self.posicion_fichas_jugador_1[1]
                self.posicion_fichas_jugador_1[1] += 10
                self.turno_fichas_jugador = 2
            elif self.turno_fichas_jugador == 2:
                x = self.posicion_fichas_jugador_2[0]
                y = self.posicion_fichas_jugador_2[1]
                self.posicion_fichas_jugador_2[1] += 10
                self.turno_fichas_jugador = 1
        elif jugador == "oponente":
            if self.turno_fichas_oponente == 1:
                x = self.posicion_fichas_oponente_1[0]
                y = self.posicion_fichas_oponente_1[1]
                self.posicion_fichas_oponente_1[1] += 10
                self.turno_fichas_oponente = 2
            elif self.turno_fichas_oponente == 2:
                x = self.posicion_fichas_oponente_2[0]
                y = self.posicion_fichas_oponente_2[1]
                self.posicion_fichas_oponente_2[1] += 10
                self.turno_fichas_oponente = 1
        label = QLabel(self)
        label.setGeometry(x, y, ancho, alto)
        pixeles = QPixmap(ruta)
        label.setPixmap(pixeles)
        label.setScaledContents(True)
        label.show()
        self.fichas.append(label)

    def usar_boton_bienestar(self):
        self.senal_boton_bienestar.emit({
            "asunto": "utilizar boton bienestar"
        })

    def respuesta_usar_boton_bienestar(self, usar):
        if usar:
            self.boton_bienestar.setEnabled(False)
        else:
            self.mensaje_boton.show()

    def resetear_ventana(self):
        self.turno_fichas_jugador = 1
        self.turno_fichas_oponente = 1
        self.boton_bienestar.setEnabled(True)
        if self.fichas:
            for ficha in self.fichas:
                ficha.clear()
        self.fichas.clear()
        self.definir_posiciones_fichas()

    def keyPressEvent(self, event):
        self.senal_tecla.emit({
            "asunto": "guardar tecla",
            "tecla": event.text().lower()
        })

    def mostrar_carta_oponente(self, ruta_carta):
        if ruta_carta is not None and ruta_carta != "":
            pixeles = QPixmap(ruta_carta)
            self.carta_oponente.setPixmap(pixeles)
            self.carta_oponente.setScaledContents(True)
        else:
            pixeles = QPixmap(self.ruta_carta_back)
            self.carta_oponente.setPixmap(pixeles)
            self.carta_oponente.setScaledContents(True)

    def ganador_juego(self):
        self.hide()
        self.resetear_ventana()
        self.timer_actualizar_ventana.stop()
        self.senal_mostrar_ventana_final.emit("jugador")

    def desconectar(self):
        self.hide()
        self.resetear_ventana()
        self.timer_actualizar_ventana.stop()
