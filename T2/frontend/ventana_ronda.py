from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import uic
import backend.parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_VENTANA_JUEGO)


class VentanaRonda(window_name, base_class):

    senal_iniciar_juego = pyqtSignal()
    senal_pausar = pyqtSignal()
    senal_avanzar = pyqtSignal()
    senal_salir = pyqtSignal()
    senal_sumar_sol = pyqtSignal(int)
    senal_seleccionar_girasol = pyqtSignal()
    senal_seleccionar_planta_clasica = pyqtSignal()
    senal_seleccionar_planta_azul = pyqtSignal()
    senal_seleccionar_patata = pyqtSignal()
    senal_seleccionar_pala = pyqtSignal()
    senal_mouse_press_event = pyqtSignal(int, int, str)
    senal_tecla = pyqtSignal(str)
    senal_enviar_datos = pyqtSignal()
    senal_stop_musica = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_gui()

    def init_gui(self):
        self.boton_iniciar.clicked.connect(self.iniciar)
        self.boton_pausa.clicked.connect(self.pausa)
        self.boton_avanzar.clicked.connect(self.avanzar)
        self.boton_salir.clicked.connect(self.salir)
        self.comprar_girasol.clicked.connect(self.seleccionar_girasol)
        self.comprar_planta_clasica.clicked.connect(self.seleccionar_planta_clasica)
        self.comprar_planta_azul.clicked.connect(self.seleccionar_planta_azul)
        self.comprar_patata.clicked.connect(self.seleccionar_patata)
        self.boton_pala.clicked.connect(self.seleccionar_pala)
        self.asignar_casillas()
    
    def configurar_timers(self):
        # Configurar timers mensajes (esconder mensajes)
        self.timer_mensaje = QTimer()
        self.timer_mensaje.setInterval(4000)
        self.timer_mensaje.timeout.connect(self.esconder_mensaje)

        self.timer_mensaje_final = QTimer()
        self.timer_mensaje_final.setInterval(5000)
        self.timer_mensaje_final.timeout.connect(self.esconder_mensaje_final)
    
    def preparar_escenario(self, escenario, nivel):
        self.resetear_ventana()
        self.setear_nivel(nivel)
        self.configurar_timers()
        if escenario == "diurno":
            self.fondo_nocturno.hide()
            self.fondo_diurno.show()
        elif escenario == "nocturno":
            self.fondo_diurno.hide()
            self.fondo_nocturno.show()
        self.crazy_cruz_chico.show()
        self.crazy_cruz_grande.hide()
        self.label_mensaje.hide()
        self.mensaje_ganar.hide()
        self.mensaje_perder.hide()
        self.boton_pausa.setEnabled(False)
        self.boton_avanzar.setEnabled(False)
        self.boton_iniciar.setEnabled(True)
        self.boton_salir.setEnabled(True)
        self.boton_pala.setEnabled(True)
        self.comprar_girasol.setEnabled(True)
        self.comprar_planta_clasica.setEnabled(True)
        self.comprar_planta_azul.setEnabled(True)
        self.comprar_patata.setEnabled(True)
        self.show()

    def setear_nivel(self, nivel):
        self.label_nivel.setText(str(nivel))
        self.label_nivel.repaint()

    def actualizar_datos(self, datos):
        self.label_soles.setText(str(datos['Soles']))
        self.label_soles.repaint()
        self.label_puntaje.setText(str(datos['Puntaje']))
        self.label_puntaje.repaint()
        self.label_zombies_destruidos.setText(str(datos['Zombies destruidos']))
        self.label_zombies_destruidos.repaint()
        self.label_zombies_restantes.setText(str(datos['Zombies restantes']))
        self.label_zombies_restantes.repaint()

    def asignar_casillas(self):
        self.labels_casillas = {
            1: self.casilla_1,
            2: self.casilla_2,
            3: self.casilla_3,
            4: self.casilla_4,
            5: self.casilla_5,
            6: self.casilla_6,
            7: self.casilla_7,
            8: self.casilla_8,
            9: self.casilla_9,
            10: self.casilla_10,
            11: self.casilla_11,
            12: self.casilla_12,
            13: self.casilla_13,
            14: self.casilla_14,
            15: self.casilla_15,
            16: self.casilla_16,
            17: self.casilla_17,
            18: self.casilla_18,
            19: self.casilla_19,
            20: self.casilla_20
        }

    def iniciar(self):
        self.boton_iniciar.setEnabled(False)
        self.boton_pausa.setEnabled(True)
        self.boton_avanzar.setEnabled(True)
        self.senal_iniciar_juego.emit()

    def pausa(self):
        self.senal_pausar.emit()

    def habilitar_botones(self, habilitar):
        if habilitar:
            self.comprar_girasol.setEnabled(True)
            self.comprar_planta_clasica.setEnabled(True)
            self.comprar_planta_azul.setEnabled(True)
            self.comprar_patata.setEnabled(True)
            self.boton_pala.setEnabled(True)
        elif not habilitar:
            self.comprar_girasol.setEnabled(False)
            self.comprar_planta_clasica.setEnabled(False)
            self.comprar_planta_azul.setEnabled(False)
            self.comprar_patata.setEnabled(False)
            self.boton_pala.setEnabled(False)

    def avanzar(self):
        self.senal_avanzar.emit()

    def salir(self):
        self.senal_pausar.emit()
        self.senal_salir.emit()
        self.hide()
        self.eliminar_objetos_ronda()
        self.resetear_ventana()
        self.senal_stop_musica.emit()

    # Mostrar mensaje chico de avisos
    def mostrar_mensaje(self, mensaje):
        self.label_mensaje.setText(mensaje)
        self.label_mensaje.repaint()
        self.label_mensaje.adjustSize()
        self.label_mensaje.show()
        self.timer_mensaje.start()

    def esconder_mensaje(self):
        self.label_mensaje.hide()
        self.timer_mensaje.stop()

    # Mostrar mensaje grande de termino de ronda
    def mostrar_mensaje_final(self, mensaje):
        self.comprar_girasol.setEnabled(False)
        self.comprar_planta_clasica.setEnabled(False)
        self.comprar_planta_azul.setEnabled(False)
        self.comprar_patata.setEnabled(False)
        self.boton_pala.setEnabled(False)
        self.boton_avanzar.setEnabled(False)
        self.boton_pausa.setEnabled(False)
        self.boton_salir.setEnabled(False)
        if mensaje == "mensaje ganar":
            self.eliminar_objetos_ronda()
            self.crazy_cruz_chico.hide()
            self.crazy_cruz_grande.show()
            self.mensaje_ganar.show()  
        elif mensaje == "mensaje perder":
            self.mensaje_perder.show() 
        self.timer_mensaje_final.start()

    def esconder_mensaje_final(self):
        self.hide()
        self.eliminar_objetos_ronda()
        self.timer_mensaje_final.stop()
        self.senal_enviar_datos.emit()

    # Crear labels plantas
    def plantar(self, ruta_planta, numero_casilla):
        label_casilla = self.labels_casillas[numero_casilla]
        pixeles = QPixmap(ruta_planta)
        label_casilla.setPixmap(pixeles)
        label_casilla.setScaledContents(True)

    # Crear labels guisantes, zombies y soles
    def crear_labels(self, tipo_objeto, numero, ruta, geometry):
        label = QLabel(self)
        label.setGeometry(geometry.x(), geometry.y(), geometry.width(), geometry.height())
        pixeles = QPixmap(ruta)
        label.setPixmap(pixeles)
        label.setScaledContents(True)
        label.show()
        if tipo_objeto == "zombie":
            self.labels_zombies[numero] = label
        elif tipo_objeto == "guisante":
            self.labels_guisantes[numero] = label
        elif tipo_objeto == "sol":
            self.labels_soles[numero] = label

    # Mover guisantes y zombies
    def actualizar_movimiento(self, datos):
        x = datos["x"]
        y = datos["y"]
        if datos["tipo objeto"] == "guisante":
            label = self.labels_guisantes[datos["numero"]]
            if datos["accion"] == "mover":
                label.move(x, y)
            elif datos["accion"] == "impactar":
                pixeles = QPixmap(datos["ruta"])
                label.setPixmap(pixeles)
                label.setScaledContents(True)
        elif datos["tipo objeto"] == "zombie":
            label = self.labels_zombies[datos["numero"]]
            pixeles = QPixmap(datos["ruta"])
            label.setPixmap(pixeles)
            label.setScaledContents(True)
            label.move(x, y)
        elif datos["tipo objeto"] =="planta":
            label = self.labels_casillas[datos["numero"]]
            pixeles = QPixmap(datos["ruta"])
            label.setPixmap(pixeles)
            label.setScaledContents(True)

    # Se esconden labels y alfinal de la ronda se eliminan
    def eliminar_label(self, tipo_objeto, numero):
        if tipo_objeto == "guisante":
            label = self.labels_guisantes[numero]
            label.hide()
        elif tipo_objeto == "zombie":
            label = self.labels_zombies[numero]
            label.hide()
        elif tipo_objeto == "planta":
            label = self.labels_casillas[numero]
            label.clear()  # Casillas no se eliminan
        elif tipo_objeto == "sol":
            label = self.labels_soles[numero]
            label.hide()

    def deterior_patata(self, numero_planta, ruta):
        label_patata = self.labels_casillas[numero_planta]
        pixeles = QPixmap(ruta)
        label_patata.setPixmap(pixeles)
        label_patata.setScaledContents(True)

    def seleccionar_girasol(self):
        self.senal_seleccionar_girasol.emit()

    def seleccionar_planta_clasica(self):
        self.senal_seleccionar_planta_clasica.emit()

    def seleccionar_planta_azul(self):
        self.senal_seleccionar_planta_azul.emit()

    def seleccionar_patata(self):
        self.senal_seleccionar_patata.emit()

    def seleccionar_pala(self):
        self.senal_seleccionar_pala.emit()

    def resetear_ventana(self):
        self.labels_zombies = {}
        self.labels_guisantes = {}
        self.labels_soles = {}
        self.ronda_pausada = True
        self.label_soles.setText(str(p.SOLES_INICIALES))
        self.label_soles.repaint()
        self.label_puntaje.setText(str(0))
        self.label_puntaje.repaint()
        self.label_zombies_destruidos.setText(str(0))
        self.label_zombies_destruidos.repaint()
        self.label_zombies_restantes.setText(str(0))
        self.label_zombies_restantes.repaint()

    def eliminar_objetos_ronda(self):
        for label in self.labels_zombies:
            label_zombie = self.labels_zombies[label]
            label_zombie.clear()
        for label in self.labels_guisantes:
            label_guisante = self.labels_guisantes[label]
            label_guisante.clear()
        for label in self.labels_soles:
            label_sol = self.labels_soles[label]
            label_sol.clear()
        for i in range(1, 21):
            self.casilla = self.labels_casillas[i]
            self.casilla.clear()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            boton = "izquierdo"
        elif event.button() == Qt.RightButton:
            boton = "derecho"
        self.senal_mouse_press_event.emit(event.x(), event.y(), boton)

    def keyPressEvent(self, event):
        self.senal_tecla.emit(event.text().lower())
