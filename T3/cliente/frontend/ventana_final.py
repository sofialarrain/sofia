from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QTimer
import os.path
from funciones import valor_parametro
from time import sleep

ruta = os.path.join(*valor_parametro("RUTA_VENTANA_FINAL"))

window_name, base_class = uic.loadUiType(ruta)


class VentanaFinal(window_name, base_class):

    senal_volver_inicio = pyqtSignal()
    senal_terminar_jugada = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_volver.clicked.connect(self.volver)
        self.mensaje_ganar.hide()
        self.mensaje_perder.hide()
        self.servidor_desconectado.hide()
        self.cerrando_programa.hide()
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.cerrar_programa)

    def mostrar_ventana(self, ganador):
        self.boton_volver.setEnabled(True)
        if ganador == "oponente":
            self.mensaje_perder.show()
        elif ganador == "jugador":
            self.mensaje_ganar.show()
        self.show()
        sleep(1)  # Espera que los dos jugadores esten en la ventana
        self.senal_terminar_jugada.emit({
            "asunto": "terminar jugada"
        })

    def volver(self):
        self.senal_volver_inicio.emit()
        self.mensaje_perder.hide()
        self.mensaje_ganar.hide()
        self.hide()

    def desconectar(self):
        self.timer.start()
        self.servidor_desconectado.show()
        self.cerrando_programa.show()
        self.mensaje_perder.hide()
        self.mensaje_ganar.hide()
        self.boton_volver.hide()
        self.show()

    def cerrar_programa(self):
        self.timer.stop()
        self.hide()
