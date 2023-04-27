import socket
from threading import Thread
from logica_servidor import LogicaServidor
import json
from cripto import encriptar, desencriptar
from funciones import valor_parametro


class Servidor:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.logica_servidor = LogicaServidor(self)
        self.id_cliente = 0
        self.sockets = {}
        self.iniciar_servidor()

    def iniciar_servidor(self):
        self.log("Cliente", "Evento", "Detalles")
        self.log("-", "Iniciando servidor", "-")
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.log("-", "Comenzado escuchar", f"Escuchando en {self.host}: {self.port}")
        self.comenzar_aceptar_clientes()

    def comenzar_aceptar_clientes(self):
        self.log("-", "Comenzando a aceptar clientes", "-")
        thread_aceptar_clientes = Thread(target=self.aceptar_clientes, daemon=True)
        thread_aceptar_clientes.start()

    def aceptar_clientes(self):
        try:
            while True:
                socket_cliente, direccion = self.socket_servidor.accept()
                self.log(
                    f"Id: {str(self.id_cliente)}", "Cliente conectado", f"Dirección: {direccion}")
                thread_escuchar_cliente = Thread(
                    target=self.escuchar_cliente,
                    args=(self.id_cliente, socket_cliente),
                    daemon=True
                )
                thread_escuchar_cliente.start()
                self.sockets[self.id_cliente] = socket_cliente
                self.id_cliente += 1
        except ConnectionError:
            self.log("-", "ERROR", "Error de conexión")

    def escuchar_cliente(self, id_cliente, socket_cliente):
        self.log(f"Id: {str(id_cliente)}", "Escuchado cliente", "-")
        try:
            while True:
                mensaje = self.recibir_mensaje(id_cliente, socket_cliente)
                if not mensaje:
                    raise ConnectionResetError
                respuesta = self.logica_servidor.procesar_mensaje(mensaje, id_cliente)
                if respuesta:
                    self.enviar_mensaje(respuesta, id_cliente, socket_cliente)
        except ConnectionError:
            self.log(f"Id: {str(id_cliente)}", "Terminando conexión cliente", "-")
            self.desconectar_cliente(id_cliente, socket_cliente)

    def recibir_mensaje(self, id_cliente, socket_cliente):
        try:
            largo_mensaje, mensaje_decodificado = self.decodificar_mensaje(socket_cliente)
            mensaje_sin_bytes_extra = mensaje_decodificado[:largo_mensaje]
            mensaje_desencriptado = desencriptar(mensaje_sin_bytes_extra)
            mensaje_deserializado = json.loads(mensaje_desencriptado.decode())
            return mensaje_deserializado
        except json.JSONDecodeError:
            self.log(f"Id: {str(id_cliente)}", "ERROR", "Error recibiendo mensaje cliente")
            raise ConnectionError()

    def enviar_mensaje(self, mensaje, id_cliente, socket_cliente):
        try:
            mensaje_serializado = json.dumps(mensaje).encode()
            mensaje_encriptado = encriptar(mensaje_serializado)
            bytes_mensaje = self.codificar_mensaje(mensaje_encriptado)
            socket_cliente.sendall(bytes_mensaje)
        except json.JSONDecodeError:
            self.log(f"Id: {str(id_cliente)}", "ERROR", "Error enviando mensaje cliente")
            raise ConnectionError()

    def codificar_mensaje(self, mensaje):
        bytes_largo_mensaje = len(mensaje).to_bytes(4, byteorder="big")
        bytes_mensaje = bytearray()
        tamano_chunck = valor_parametro("TAMANO_CHUNCK")
        numero_bloque = 1
        posicion = 0
        contador = 0
        while contador < len(mensaje):
            bytes_numero_bloque = numero_bloque.to_bytes(4, byteorder="little")
            tamano_bloque = min(tamano_chunck, len(mensaje) - contador)
            contador += tamano_bloque
            chunck = mensaje[posicion:(posicion + tamano_bloque)]
            while len(chunck) % tamano_chunck != 0:
                chunck += b'\x00'
            bytes_mensaje += (bytes_numero_bloque + chunck)
            posicion += tamano_chunck
            numero_bloque += 1
        mensaje_codificado = (bytes_largo_mensaje + bytes_mensaje)
        return mensaje_codificado

    def decodificar_mensaje(self, socket_cliente):
        try:
            bytes_largo_mensaje = socket_cliente.recv(4)
            # Largo mensaje original
            largo_mensaje = int.from_bytes(bytes_largo_mensaje, byteorder="big")
            bytes_mensaje = bytearray()
            # Largo bytes que contienen mensaje original
            largo_bytes = 0
            contador = 0
            tamano_chunck = valor_parametro("TAMANO_CHUNCK")
            while contador < largo_mensaje:
                contador += tamano_chunck
                largo_bytes += (tamano_chunck + 4)
            while len(bytes_mensaje) < largo_bytes:
                chunk = min(largo_bytes - len(bytes_mensaje), tamano_chunck)
                bytes_mensaje += socket_cliente.recv(chunk)
            turno = "bloque"
            mensaje_decodificado = bytearray()
            posicion = 0
            n_bloque = 1
            while posicion < len(bytes_mensaje):
                if turno == "bloque":
                    bytes_numero_bloque = bytes_mensaje[posicion:(posicion + 4)]
                    numero_bloque = int.from_bytes(bytes_numero_bloque, byteorder="little")
                    posicion += 4
                    turno = "chunck"
                elif turno == "chunck":
                    if numero_bloque == n_bloque:  # Chequear bloque
                        mensaje_decodificado += bytes_mensaje[posicion:(posicion + tamano_chunck)]
                        posicion += tamano_chunck
                        turno = "bloque"
                        n_bloque += 1
                    else:
                        raise ConnectionAbortedError()
            return largo_mensaje, mensaje_decodificado
        except ConnectionAbortedError:
            self.log("-", "Error decodificación mensaje", "")
            return 0, b""

    def desconectar_cliente(self, id_cliente, socket_cliente):
        try:
            self.log(f"Id: {str(id_cliente)}", "Desconectando cliente", "Borrando socket cliente")
            socket_cliente.close()
            self.sockets.pop(id_cliente, None)
            self.logica_servidor.eliminar_jugador(id_cliente)
        except KeyError:
            self.log(f"Id: {str(id_cliente)}", "Error desconexion cliente", "-")

    def log(self, cliente: str, evento: str, detalle: str):
        str_cliente = cliente.center(40, " ")
        str_evento = evento.center(40, " ")
        str_detalle = detalle.center(40, " ")
        lineas = ("-" * 40)
        print(str_cliente + "|" + str_evento + "|" + str_detalle)
        print(lineas + "|" + lineas + "|" + lineas)

    def cerrar_servidor(self):
        self.socket_servidor.close()
