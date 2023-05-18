from typing import List
import json

##################
## Encriptar    ##
##################


def serializar_diccionario(dictionary: dict) -> bytearray:
    return bytearray(json.dumps(dictionary).encode("utf-8"))


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    if len(secuencia) > len(mensaje):
        raise ValueError(
            "La secuencia no puede ser más larga que el mensaje a encriptar"
        )

    if max(secuencia) >= len(mensaje):
        raise ValueError(
            "La secuencia no puede contener un número igual o mayor al largo del mensaje a encriptar"
        )
    if len(set(secuencia)) != len(secuencia):
        raise ValueError("La secuencia debe contener solo valores únicos.")


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    position_message = bytearray()
    for x in secuencia:
        position_message.extend(int.to_bytes(x, 2, "big"))
    return position_message


def codificar_largo(largo: int) -> bytearray:
    return bytearray(int.to_bytes(largo, 4, "big"))


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    extracted_message = bytearray()
    original_message = bytearray()
    for x in secuencia:
        extracted_message.append(mensaje[x])

    for i, x in enumerate(mensaje):
        if i not in secuencia:
            original_message.append(x)

    return [extracted_message, original_message]


def codificar_separador(chunk_1: bytearray, chunk_2: bytearray) -> bytearray:
    suma = chunk_1[0] + chunk_1[-1] + chunk_2[0] + chunk_2[-1]
    return suma % 2 == 0  # es par


def encriptar(mensaje: bytearray, secuencia: List[int]) -> bytearray:
    try:
        verificar_secuencia(mensaje, secuencia)
    except ValueError:
        return

    extracted_message, original_message = separar_msg(
        mensaje, secuencia)
    position_message = codificar_secuencia(secuencia)

    separador = codificar_separador(extracted_message, original_message)
    if separador:  # es par
        return (
            bytearray(int.to_bytes(0, 1, "big"))
            + codificar_largo(len(secuencia))
            + extracted_message
            + original_message
            + position_message
        )
    else:  # Es impar
        return (
            bytearray(int.to_bytes(1, 1, "big"))
            + codificar_largo(len(secuencia))
            + original_message
            + position_message
            + extracted_message
        )

#####################
## Desencriptar    ##
#####################


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    return json.loads(mensaje_codificado.decode("utf-8"))


def decodificar_largo(mensaje: bytearray) -> int:
    return int.from_bytes(mensaje[1:5], "big")


def decodificar_separador(mensaje: bytearray) -> int:
    return int.from_bytes(mensaje[0:1], "big")


def separar_msg_caso_par(mensaje: bytearray, largo: int) -> List[bytearray]:
    extracted_message = mensaje[5: largo + 5]
    original_message = mensaje[5 + largo: -2 * largo]
    secuencia_codificada = mensaje[-2 * largo:]
    return [extracted_message, original_message, secuencia_codificada]


def separar_msg_caso_impar(mensaje: bytearray, largo: int) -> List[bytearray]:
    original_message = mensaje[5: -3*largo]
    secuencia_codificada = mensaje[-3*largo: -largo]
    extracted_message = mensaje[-largo:]
    return [extracted_message, original_message, secuencia_codificada]


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    separador = decodificar_separador(mensaje)
    length = decodificar_largo(mensaje)
    if separador == 0:
        return separar_msg_caso_par(mensaje, length)
    else:
        return separar_msg_caso_impar(mensaje, length)


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    secuencia = []
    for i in range(0, len(secuencia_codificada), 2):
        numero = int.from_bytes(secuencia_codificada[i: i + 2], "big")
        secuencia.append(numero)

    return secuencia


def desencriptar(mensaje: bytearray) -> bytearray:
    chunk_1, chunk_2, secuencia_codificada = separar_msg_encriptado(mensaje)

    secuencia = decodificar_secuencia(secuencia_codificada)
    secrect_message = {}
    for i in range(len(secuencia)):
        secrect_message[secuencia[i]] = chunk_1[i]

    index = 0
    final_message = bytearray()
    for i in range(len(secuencia) + len(chunk_2)):
        if i in secrect_message:
            final_message.append(secrect_message[i])
        else:
            final_message.append(chunk_2[index])
            index += 1

    return final_message


if __name__ == "__main__":
    original = serializar_diccionario({"anya": 1})
    encriptado = encriptar(original, [1, 5, 4, 3, 8, 9, 0, 2, 6, 7])
    desencriptado = desencriptar(encriptado)
    diccionario = deserializar_diccionario(desencriptado)
    print(encriptado)
    print(original == desencriptado, diccionario)

    original = serializar_diccionario({"anya": 1})
    encriptado = encriptar(original, [1, 5, 4, 3, 8, 9, 0, 2, 6])
    desencriptado = desencriptar(encriptado)
    diccionario = deserializar_diccionario(desencriptado)
    print(encriptado)
    print(original == desencriptado, diccionario)
