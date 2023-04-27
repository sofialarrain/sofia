from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
import os.path
from funciones import valor_parametro


ruta = os.path.join(*valor_parametro("RUTA_VENTANA_INICIO"))

window_name, base_class = uic.loadUiType(ruta)


class VentanaInicio(window_name, base_class):

    senal_validar_usuario = pyqtSignal(dict)
    senal_ingresar_sala_espera = pyqtSignal(dict)
    senal_mostrar_ventana_espera = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.setMouseTracking(True)
        self.fondo.setMouseTracking(True)
        self.puerta.clicked.connect(self.validar_usuario)

    def mostrar_ventana(self):
        self.mensaje_juego_en_curso.hide()
        self.mensaje_sin_capacidad.hide()
        self.puerta.hide()
        self.usuario.setText("")  # Resetear 
        self.usuario.setPlaceholderText(" Ingresa tu nombre...")
        self.show()

    def validar_usuario(self):
        self.nombre_usuario = self.usuario.text()
        self.senal_validar_usuario.emit({
            "asunto": "validar usuario",
            "usuario": self.nombre_usuario
        })

    def recibir_validacion_usuario(self, valido, error):
        if valido:
            self.senal_ingresar_sala_espera.emit({
                "asunto": "ingresar sala espera",
                "usuario": self.nombre_usuario
            })
            self.usuario.setText("")
            self.usuario.setPlaceholderText(" Usuario válido")
        else:
            if error == "rango":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" [Error] No cumple rango")
            elif error == "alfanumerico":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" [Error] Debe ser alfanumérico")
            elif error == "existe":
                self.usuario.setText("")
                self.usuario.setPlaceholderText(" [Error] Nombre ya registrado")

    def recibir_ingreso_ventana_espera(self, ingresar, error):
        if ingresar:
            self.hide()
            self.senal_mostrar_ventana_espera.emit(self.nombre_usuario)
        else:
            if error == "juego en curso":
                self.mensaje_juego_en_curso.show()
                self.mensaje_sin_capacidad.hide()
            elif error == "sin capacidad":
                self.mensaje_sin_capacidad.show()
                self.mensaje_juego_en_curso.hide()

    def mouseMoveEvent(self, event):
        geometry_puerta = valor_parametro("GEOMETRY_PUERTA_INICIO")
        ancho_puerta = [geometry_puerta[0], geometry_puerta[0] + geometry_puerta[2]]
        alto_puerta = [geometry_puerta[1], geometry_puerta[1] + geometry_puerta[3]]
        if (event.x() in range(ancho_puerta[0], ancho_puerta[1])):
            if (event.y() in range(alto_puerta[0], alto_puerta[1])):
                self.puerta.show()
            else:
                self.puerta.hide()
        else:
            self.puerta.hide()

    def desconectar(self):
        self.hide()
