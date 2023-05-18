from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    # Completar
    pass


def decodificar_largo(mensaje: bytearray) -> int:
    # Completar
    pass


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_nuevo = bytearray()
    m_original = bytearray()
    secuencia_codificada = bytearray()
    # Completar

    return [m_nuevo, m_original, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    # Completar
    pass


def desencriptar(mensaje: bytearray) -> bytearray:
    # Completar
    pass


if __name__ == "__main__":
    mensaje = bytearray(
        b'\x00\x00\x00\x0b"ayn }1{a":\x00\x01\x00\x05\x00\x04\x00\x03\x00\
            \x08\x00\n\x00\t\x00\x00\x00\x02\x00\x06\x00\x07')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
