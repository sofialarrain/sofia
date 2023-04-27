from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from PyQt5.QtMultimedia import QSound
import backend.parametros as p


window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_PRINCIPAL)

class VentanaPrincipal(window_name, base_class):

    senal_iniciar = pyqtSignal(str, str, int, int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_iniciar.clicked.connect(self.iniciar)
        self.boton_diurno.clicked.connect(self.definir_escenario_diurno)
        self.boton_nocturno.clicked.connect(self.definir_escenario_nocturno)

    def mostrar_ventana(self, usuario, nivel, puntaje):
        self.boton_iniciar.setEnabled(False)
        self.musica = QSound(p.RUTA_MUSICA_2)
        self.musica.play()
        self.usuario = usuario
        self.nivel = nivel
        self.puntaje = puntaje
        self.show()
    
    def definir_escenario_diurno(self):
        self.escenario = "diurno"
        self.boton_iniciar.setEnabled(True)
    
    def definir_escenario_nocturno(self):
        self.escenario = "nocturno"
        self.boton_iniciar.setEnabled(True)
        
    def iniciar(self):
        self.boton_diurno.setCheckable(False)
        self.boton_diurno.setCheckable(True)
        self.boton_nocturno.setCheckable(False)
        self.boton_nocturno.setCheckable(True)
        self.hide()
        self.musica.stop()
        self.senal_iniciar.emit(self.usuario, self.escenario, self.nivel, self.puntaje)
