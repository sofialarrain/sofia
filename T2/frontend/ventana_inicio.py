from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic
import backend.parametros as p


window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_INICIO)

class VentanaInicio(window_name, base_class):

    senal_musica = pyqtSignal()
    senal_enviar_usuario = pyqtSignal(str)
    senal_mostrar_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_jugar.clicked.connect(self.jugar)
        self.boton_ranking.clicked.connect(self.ranking)
        self.boton_salir.clicked.connect(self.salir)

    def mostrar_ventana(self):
        self.usuario.setText("")  # Resetear para cuando vuelva a inicio
        self.usuario.setPlaceholderText("Introduzca usuario")
        self.senal_musica.emit()
        self.show()
    
    def recibir_validacion_usuario(self, valido, error):
        if valido:
            self.senal_musica.emit()
            self.hide()
        else:
            if error == "rango":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" Error. No cumple rango")
            elif error == "vacio":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" Error. No puede ser vacio")
            elif error == "alfanumérico":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" Error. Debe ser alfanumérico")
            elif error == "espacio":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" Error. No puede contener espacios")

    def jugar(self):
        self.senal_enviar_usuario.emit(self.usuario.text())

    def ranking(self):
        self.senal_musica.emit()
        self.senal_mostrar_ranking.emit()
        self.hide()

    def salir(self):
        self.senal_musica.emit()
        self.hide()