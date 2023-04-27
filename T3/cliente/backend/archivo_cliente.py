from PyQt5.QtCore import pyqtSignal, QObject
import socket
import json
from threading import Thread
from backend.cripto import encriptar, desencriptar
from funciones import valor_parametro


class Cliente(QObject):

    senal_mostrar_ventana_inicio = pyqtSignal()
    senal_operar_mensaje = pyqtSignal(dict)
    senal_desconectar_servidor = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = None

    def iniciando_cliente(self):
        try:
            self.socket.connect((self.host, self.port))
            self.conectado = True
            print("Conectando cliente a servidor.")
            self.senal_mostrar_ventana_inicio.emit()
            self.comenzar_escuchar()
        except ConnectionError:
            self.conectado = False
            print("Error. Problemas de conexión con el servidor.")
            self.socket.close()

    def comenzar_escuchar(self):
        thread_escuchar = Thread(target=self.escuchar_servidor, daemon=True)
        thread_escuchar.start()
        print("Comenzando a escuchar servidor.")

    def escuchar_servidor(self):
        try:
            while self.conectado:
                mensaje = self.recibir_mensaje()
                if mensaje:
                    self.senal_operar_mensaje.emit(mensaje)
                    if mensaje["asunto"] == "ingresar sala espera":
                        self.id = mensaje["id"]
        except ConnectionError:
            self.senal_desconectar_servidor.emit()
            print("Error. Se ha perdido la conexión con el servidor.")

    def recibir_mensaje(self):
        try:
            largo_mensaje, mensaje_decodificado = self.decodificar_mensaje()
            mensaje_sin_bytes_extra = mensaje_decodificado[:largo_mensaje]
            mensaje_desencriptado = desencriptar(mensaje_sin_bytes_extra)
            mensaje_deserializado = json.loads(mensaje_desencriptado.decode())
            return mensaje_deserializado
        except json.JSONDecodeError:
            print("Error recibiendo mensaje servidor.")
            raise ConnectionError()

    def enviar_mensaje(self, mensaje):
        try:
            mensaje_serializado = json.dumps(mensaje).encode()
            mensaje_encriptado = encriptar(mensaje_serializado)
            mensaje_codificado = self.codificar_mensaje(mensaje_encriptado)
            self.socket.sendall(mensaje_codificado)
        except json.JSONDecodeError:
            print("Error enviando mensaje a servidor.")
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

    def decodificar_mensaje(self):
        try:
            bytes_largo_mensaje = self.socket.recv(4)
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
                bytes_mensaje += self.socket.recv(chunk)
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
            print("ERROR. No se ha podido decodificar mensaje de servidor.")
            return 0, b""

    def cerrar_socket(self):
        self.socket.close()
        print("Cerrando socket cliente.")
