from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        return bytearray(json.dumps(dictionary).encode("utf-8"))
    except TypeError:
        raise JsonError()


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    if len(secuencia) > len(mensaje):
        raise SequenceError()
    if max(secuencia) >= len(mensaje):
        raise SequenceError()
    if len(set(secuencia)) != len(secuencia):
        raise SequenceError()


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    position_message = bytearray()
    for x in secuencia:
        position_message.extend(int.to_bytes(x, 2, "big"))
    return position_message


def codificar_largo(largo: int) -> bytearray:
    return bytearray(int.to_bytes(largo, 4, "big"))


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_nuevo = bytearray()
    m_original = bytearray()
    for x in secuencia:
        m_nuevo.append(mensaje[x])

    for i, x in enumerate(mensaje):
        if i not in secuencia:
            m_original.append(x)

    return [m_nuevo, m_original]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_nuevo, m_original = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_nuevo
        + m_original
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"anya": 1})
    encriptado = encriptar(original, [1, 5, 4, 3, 8, 10, 9, 0, 2, 6, 7])
    print(encriptado)
    print(original)
