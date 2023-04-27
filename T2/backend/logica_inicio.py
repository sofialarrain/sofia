from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtMultimedia import QSound
import backend.parametros as p


class LogicaInicio(QObject):

    senal_respuesta_validacion = pyqtSignal(bool, str)
    senal_abrir_juego = pyqtSignal(str, int, int)

    def __init__(self):
        super().__init__()
        self.musica_corriendo = False
        self.musica = QSound(p.RUTA_MUSICA_1)

    def validar_usuario(self, usuario):
        if not (usuario.isdigit()):
            if " " in usuario:
                self.senal_respuesta_validacion.emit(False, "espacio")
            else:
                if len(usuario) >= p.MIN_CARACTERES and len(usuario) <= p.MAX_CARACTERES:
                    self.senal_respuesta_validacion.emit(True, "")
                    self.senal_abrir_juego.emit(usuario, 1, 0)
                else:
                    if len(usuario) == 0:
                        self.senal_respuesta_validacion.emit(False, "vacio")
                    else:
                        self.senal_respuesta_validacion.emit(False, "rango")
        else:
            self.senal_respuesta_validacion.emit(False, "alfanumérico")
    
    def musica_ventana(self):
        if not self.musica_corriendo:
            self.musica.play()
            self.musica_corriendo = True
        else:
            self.musica_corriendo = False
            self.musica.stop()
