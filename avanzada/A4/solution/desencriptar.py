from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    try:
        return json.loads(mensaje_codificado.decode("utf-8"))
    except json.JSONDecodeError:
        raise JsonError()


def decodificar_largo(mensaje: bytearray) -> int:
    return int.from_bytes(mensaje[0:4], "big")


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    length = decodificar_largo(mensaje)
    m_nuevo = mensaje[4: length + 4]
    m_original = mensaje[4 + length: -2 * length]
    secuencia_codificada = mensaje[-2 * length:]
    return [m_nuevo, m_original, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    secuencia = []
    for i in range(0, len(secuencia_codificada), 2):
        numero = int.from_bytes(secuencia_codificada[i: i + 2], "big")
        secuencia.append(numero)

    return secuencia


def desencriptar(mensaje: bytearray) -> bytearray:
    m_nuevo, m_original, secuencia_codificada = separar_msg_encriptado(mensaje)

    secuencia = decodificar_secuencia(secuencia_codificada)
    secrect_message = {}
    for i in range(len(secuencia)):
        secrect_message[secuencia[i]] = m_nuevo[i]

    index = 0
    final_message = bytearray()
    for i in range(len(secuencia) + len(m_original)):
        if i in secrect_message:
            final_message.append(secrect_message[i])
        else:
            final_message.append(m_original[index])
            index += 1

    return final_message


if __name__ == "__main__":
    mensaje = bytearray(
        b'\x00\x00\x00\x0b"ayn }1{a":\x00\x01\x00\x05\x00\x04\x00\x03\x00\
            \x08\x00\n\x00\t\x00\x00\x00\x02\x00\x06\x00\x07')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
