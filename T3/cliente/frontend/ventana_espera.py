from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
import os.path
from funciones import valor_parametro

ruta = os.path.join(*valor_parametro("RUTA_VENTANA_ESPERA"))

window_name, base_class = uic.loadUiType(ruta)


class VentanaEspera(window_name, base_class):

    senal_volver = pyqtSignal()
    senal_actualizar_ventana = pyqtSignal(dict)
    senal_mostrar_ventana_juego = pyqtSignal(str, str)
    senal_salir_sala_espera = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.oponente = None
        self.cuenta_regresiva = valor_parametro("CUENTA_REGRESIVA_INICIO")
        self.init_gui()
        self.configurar_timer()

    def init_gui(self):
        self.boton_volver.clicked.connect(self.volver)

    def configurar_timer(self):
        # Timer actualización ventana
        self.timer_actualizar_ventana = QTimer()
        self.timer_actualizar_ventana.setInterval(valor_parametro("INTERVALO_ACTUALIZAR_VENTANA"))
        self.timer_actualizar_ventana.timeout.connect(self.actualizar_ventana)

    def actualizar_ventana(self):
        self.senal_actualizar_ventana.emit({
            "asunto": "actualizar ventana",
            "estado": "sala espera",
            "oponente": self.oponente
        })

    def mostrar_ventana(self, usuario):
        self.jugador = usuario
        self.nombre_jugador.setText(usuario)
        self.timer_actualizar_ventana.start()
        self.show()

    def esconder_ventana(self):
        self.timer_actualizar_ventana.stop()
        self.hide()
        self.nombre_oponente.setText("Esperando oponente...")
        self.senal_mostrar_ventana_juego.emit(self.jugador, self.oponente)

    def actualizar_tiempo(self, segundo):
        self.segundos.setText(str(segundo))

    def recibir_oponente(self, oponente):
        self.oponente = oponente
        self.nombre_oponente.setText(oponente)

    def oponente_desconectado(self):
        self.oponente = None
        self.nombre_oponente.setText("Esperando oponente...")
        self.segundos.setText(str(valor_parametro("CUENTA_REGRESIVA_INICIO")))

    def volver(self):
        self.senal_volver.emit()
        self.senal_salir_sala_espera.emit({
            "asunto": "salir sala espera"
        })
        self.hide()

    def desconectar(self):
        self.timer_actualizar_ventana.stop()
        self.hide()
        self.nombre_oponente.setText("Esperando oponente...")
