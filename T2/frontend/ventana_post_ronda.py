from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import backend.parametros as p
from PyQt5.QtMultimedia import QSound

window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_POST_RONDA)


class VentanaPostRonda(window_name, base_class):

    senal_siguiente_ronda = pyqtSignal(str, int, int)
    senal_salir = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_siguiente_ronda.clicked.connect(self.siguiente_ronda)
        self.boton_salir.clicked.connect(self.salir)
        self.musica = QSound(p.RUTA_MUSICA_2)
    
    def mostrar_ventana(self, resultados):
        self.usuario = resultados['Usuario']
        self.nivel = resultados['Ronda actual']
        self.puntaje = resultados['Puntaje total']
        self.actualizar_ventana(resultados)
        self.musica.play()
        self.show()
    
    def actualizar_ventana(self, resultados):
        self.ronda_actual.setText(str(resultados['Ronda actual']))
        self.soles_restantes.setText(str(resultados['Soles restantes']))
        self.zombies_destruidos.setText(str(resultados['Zombies destruidos']))
        self.puntaje_ronda.setText(str(resultados['Puntaje ronda']))
        self.puntaje_total.setText(str(resultados['Puntaje total']))
        if resultados['Estado ronda'] == "ganada":
            self.mensaje_ganar.show()
            self.mensaje_perder.hide()
        elif resultados['Estado ronda'] == "perdida":
            self.mensaje_perder.show()
            self.mensaje_ganar.hide()
            self.boton_siguiente_ronda.hide()
    
    def siguiente_ronda(self):
        self.musica.stop()
        self.hide()
        self.senal_siguiente_ronda.emit(self.usuario, self.nivel + 1, self.puntaje)
    
    def salir(self):
        self.musica.stop()
        self.hide()
        self.senal_salir.emit()
