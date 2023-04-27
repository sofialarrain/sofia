from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import backend.parametros as p


window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_RANKING)


class VentanaRanking(window_name, base_class):

    senal_volver = pyqtSignal()
    senal_actualizar_ventana = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_volver.clicked.connect(self.volver)

    def mostrar_ventana(self):
        self.senal_actualizar_ventana.emit()
        self.show()
        
    def volver(self):
        self.hide()
        self.senal_volver.emit()
    
    def actualizar(self, ranking):
        if len(ranking) >= 1:
            self.usuario_1.setText(ranking[0][0])
            self.usuario_1.adjustSize()
            self.puntaje_1.setText(str(ranking[0][1]))
            self.puntaje_1.adjustSize()
        if len(ranking) >= 2:
            self.usuario_2.setText(ranking[1][0])
            self.usuario_2.adjustSize()
            self.puntaje_2.setText(str(ranking[1][1]))
            self.puntaje_2.adjustSize()
        if len(ranking) >= 3:
            self.usuario_3.setText(ranking[2][0])
            self.usuario_3.adjustSize()
            self.puntaje_3.setText(str(ranking[2][1]))
            self.puntaje_3.adjustSize()
        if len(ranking) >= 4:
            self.usuario_4.setText(ranking[3][0])
            self.usuario_4.adjustSize()
            self.puntaje_4.setText(str(ranking[3][1]))
            self.puntaje_4.adjustSize()
        if len(ranking) >= 5:
            self.usuario_5.setText(ranking[4][0])
            self.usuario_5.adjustSize()
            self.puntaje_5.setText(str(ranking[4][1]))
            self.puntaje_5.adjustSize()

