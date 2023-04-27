from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_ronda import VentanaRonda
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_post_ronda import VentanaPostRonda
from backend.logica_inicio import LogicaInicio
from backend.logica_ronda import LogicaRonda
from backend.logica_ranking import LogicaRanking


class DCCruzVsZombies(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        # Ventanas
        self.ventana_inicio = VentanaInicio()
        self.ventana_ronda = VentanaRonda()
        self.ventana_ranking = VentanaRanking()
        self.ventana_principal = VentanaPrincipal()
        self.ventana_post_ronda = VentanaPostRonda()

        # Lógicas
        self.logica_inicio = LogicaInicio()
        self.logica_ronda = LogicaRonda()
        self.logica_ranking = LogicaRanking()
        
        # Señales
        self.conectar_inicio()
        self.conectar_ranking()
        self.conectar_principal()
        self.conectar_ronda()
        self.conectar_post_ronda()

    def conectar_inicio(self):
        # Señales Ventana Inicio
        self.ventana_inicio.senal_enviar_usuario.connect(self.logica_inicio.validar_usuario)
        self.ventana_inicio.senal_mostrar_ranking.connect(self.ventana_ranking.mostrar_ventana)
        self.ventana_inicio.senal_musica.connect(self.logica_inicio.musica_ventana)

        # Señales Lógica Inicio
        self.logica_inicio.senal_respuesta_validacion.connect(
            self.ventana_inicio.recibir_validacion_usuario)
        self.logica_inicio.senal_abrir_juego.connect(self.ventana_principal.mostrar_ventana)
    
    def conectar_ranking(self):
        # Señales Ventana Ranking
        self.ventana_ranking.senal_volver.connect(self.ventana_inicio.mostrar_ventana)
        self.ventana_ranking.senal_actualizar_ventana.connect(
            self.logica_ranking.actualizar_ventana)

        # Señales Lógica Ranking
        self.logica_ranking.senal_actualizar.connect(self.ventana_ranking.actualizar)
        
    def conectar_principal(self):
        # Señales Ventana Principal
        self.ventana_principal.senal_iniciar.connect(self.logica_ronda.preparar_ronda)

    def conectar_ronda(self):
        # Señales Ventana Ronda
        self.ventana_ronda.senal_iniciar_juego.connect(self.logica_ronda.iniciar)
        self.ventana_ronda.senal_pausar.connect(self.logica_ronda.pausar)
        self.ventana_ronda.senal_salir.connect(self.ventana_inicio.mostrar_ventana)
        self.ventana_ronda.senal_avanzar.connect(self.logica_ronda.avanzar)
        self.ventana_ronda.senal_seleccionar_girasol.connect(
            self.logica_ronda.seleccionar_girasol)
        self.ventana_ronda.senal_seleccionar_planta_clasica.connect(
            self.logica_ronda.seleccionar_planta_clasica)
        self.ventana_ronda.senal_seleccionar_planta_azul.connect(
            self.logica_ronda.seleccionar_planta_azul)
        self.ventana_ronda.senal_seleccionar_patata.connect(
            self.logica_ronda.seleccionar_patata)
        self.ventana_ronda.senal_seleccionar_pala.connect(
            self.logica_ronda.seleccionar_pala)
        self.ventana_ronda.senal_mouse_press_event.connect(
            self.logica_ronda.revisar_mouse_press_event)
        self.ventana_ronda.senal_tecla.connect(self.logica_ronda.revisar_tecla)
        self.ventana_ronda.senal_enviar_datos.connect(self.logica_ronda.enviar_datos)
        self.ventana_ronda.senal_stop_musica.connect(self.logica_ronda.stop_musica)

        # Señales Lógica Ronda
        self.logica_ronda.senal_actualizar_datos.connect(self.ventana_ronda.actualizar_datos)
        self.logica_ronda.senal_preparar_escenario.connect(self.ventana_ronda.preparar_escenario)
        self.logica_ronda.senal_plantar.connect(self.ventana_ronda.plantar)
        self.logica_ronda.senal_crear_label.connect(self.ventana_ronda.crear_labels)
        self.logica_ronda.senal_actualizar_movimientos.connect(
            self.ventana_ronda.actualizar_movimiento)
        self.logica_ronda.senal_eliminar_objeto.connect(self.ventana_ronda.eliminar_label)
        self.logica_ronda.senal_deteriorar_patata.connect(self.ventana_ronda.deterior_patata)
        self.logica_ronda.senal_mensaje.connect(self.ventana_ronda.mostrar_mensaje)
        self.logica_ronda.senal_mensaje_final.connect(self.ventana_ronda.mostrar_mensaje_final)
        self.logica_ronda.senal_terminar_ronda.connect(self.ventana_post_ronda.mostrar_ventana)
        self.logica_ronda.senal_habilitar_botones.connect(self.ventana_ronda.habilitar_botones)
        self.logica_ronda.senal_actualizar_ranking.connect(self.logica_ranking.actualizar_ranking)

    def conectar_post_ronda(self):
        # Señales Ventana Post Ronda
        self.ventana_post_ronda.senal_siguiente_ronda.connect(
            self.ventana_principal.mostrar_ventana)
        self.ventana_post_ronda.senal_salir.connect(self.ventana_inicio.mostrar_ventana)

    def iniciar(self):
        # Iniciar juego
        self.ventana_inicio.mostrar_ventana()
