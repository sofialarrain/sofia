from backend.conecciones import DCCruzVsZombies
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    juego = DCCruzVsZombies(sys.argv)
    juego.iniciar()
    sys.exit(app.exec())
