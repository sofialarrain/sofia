from PyQt5.QtWidgets import QApplication
from backend.archivo_cliente import Cliente
from backend.interfaz import Interfaz
import socket
import sys
from funciones import valor_parametro

if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = valor_parametro("PORT")
    try:
        app = QApplication(sys.argv)
        interfaz = Interfaz()
        cliente = Cliente(HOST, PORT)

        # Señales Cliente
        cliente.senal_mostrar_ventana_inicio.connect(interfaz.ventana_inicio.mostrar_ventana)
        cliente.senal_operar_mensaje.connect(interfaz.operar_mensaje)
        cliente.senal_desconectar_servidor.connect(interfaz.ventana_inicio.desconectar)
        cliente.senal_desconectar_servidor.connect(interfaz.ventana_espera.desconectar)
        cliente.senal_desconectar_servidor.connect(interfaz.ventana_juego.desconectar)
        cliente.senal_desconectar_servidor.connect(interfaz.ventana_final.desconectar)

        # Señales Ventana Inicio
        interfaz.ventana_inicio.senal_validar_usuario.connect(cliente.enviar_mensaje)
        interfaz.ventana_inicio.senal_ingresar_sala_espera.connect(cliente.enviar_mensaje)
        interfaz.ventana_inicio.senal_mostrar_ventana_espera.connect(
            interfaz.ventana_espera.mostrar_ventana)

        # Señales Ventana Espera
        interfaz.ventana_espera.senal_volver.connect(interfaz.ventana_inicio.mostrar_ventana)
        interfaz.ventana_espera.senal_salir_sala_espera.connect(cliente.enviar_mensaje)
        interfaz.ventana_espera.senal_actualizar_ventana.connect(cliente.enviar_mensaje)
        interfaz.ventana_espera.senal_mostrar_ventana_juego.connect(
            interfaz.ventana_juego.mostrar_ventana)

        # Señales Ventana Juego
        interfaz.ventana_juego.senal_carta_bandeja.connect(cliente.enviar_mensaje)
        interfaz.ventana_juego.senal_actualizar_ventana.connect(cliente.enviar_mensaje)
        interfaz.ventana_juego.senal_carta_elegida.connect(cliente.enviar_mensaje)
        interfaz.ventana_juego.senal_mostrar_ventana_final.connect(
            interfaz.ventana_final.mostrar_ventana)
        interfaz.ventana_juego.senal_boton_bienestar.connect(cliente.enviar_mensaje)
        interfaz.ventana_juego.senal_tecla.connect(cliente.enviar_mensaje)

        # Señales Ventana Final
        interfaz.ventana_final.senal_volver_inicio.connect(interfaz.ventana_inicio.mostrar_ventana)
        interfaz.ventana_final.senal_terminar_jugada.connect(cliente.enviar_mensaje)

        # Señales Interfaz
        interfaz.senal_respuesta_validacion.connect(
            interfaz.ventana_inicio.recibir_validacion_usuario)
        interfaz.senal_respuesta_ingreso_sala_espera.connect(
            interfaz.ventana_inicio.recibir_ingreso_ventana_espera)
        interfaz.senal_actualizar_segundos_sala_espera.connect(
            interfaz.ventana_espera.actualizar_tiempo)
        interfaz.senal_oponente_conectado.connect(interfaz.ventana_espera.recibir_oponente)
        interfaz.senal_oponente_desconectado.connect(interfaz.ventana_espera.oponente_desconectado)
        interfaz.senal_actualizar_segundos_ronda.connect(interfaz.ventana_juego.actualizar_tiempo)
        interfaz.senal_actualizar_carta.connect(interfaz.ventana_juego.actualizar_carta)
        interfaz.senal_actualizar_ronda_actual.connect(
            interfaz.ventana_juego.actualizar_ronda_actual)
        interfaz.senal_mostrar_ganador_ronda.connect(interfaz.ventana_juego.mostrar_ganador_ronda)
        interfaz.senal_agregar_ficha.connect(interfaz.ventana_juego.agregar_ficha)
        interfaz.senal_regresar_ronda.connect(interfaz.ventana_juego.preparar_ronda)
        interfaz.senal_respuesta_boton_bienestar.connect(
            interfaz.ventana_juego.respuesta_usar_boton_bienestar)
        interfaz.senal_mostrar_carta_oponente.connect(interfaz.ventana_juego.mostrar_carta_oponente)
        interfaz.senal_ganador_juego.connect(interfaz.ventana_juego.ganador_juego)

        # Iniciar cliente (mostrar ventana inicio)
        cliente.iniciando_cliente()
        sys.exit(app.exec_())

    except ConnectionError:
        print("Error de conexión")
    except KeyboardInterrupt:
        print("Desconectando cliente...")
        cliente.cerrar_socket()
        sys.exit()
