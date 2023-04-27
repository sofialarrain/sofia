"""
Módulo principal del servidor
"""
import sys
from archivo_servidor import Servidor
import socket
from funciones import valor_parametro

if __name__ == "__main__":
    HOST = socket.gethostname()
    PORT = valor_parametro("PORT")

    print("Abriendo servidor...")
    servidor = Servidor(HOST, PORT)
    try:
        while True:
            input()
    except KeyboardInterrupt:
        print("Cerrando servidor...")
        servidor.cerrar_servidor()
        sys.exit()
