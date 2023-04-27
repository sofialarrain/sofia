import math


def encriptar(msg: bytearray) -> bytearray:
    largo_mensaje = len(msg)
    parte_A = bytearray()
    parte_B = bytearray()
    parte_C = bytearray()
    turno = "A"
    for i in range(largo_mensaje):
        if turno == "A":
            n = msg[i]
            byte = n.to_bytes(1, "little")
            parte_A += byte
            turno = "B"
        elif turno == "B":
            n = msg[i]
            byte = n.to_bytes(1, "little")
            parte_B += byte
            turno = "C"
        elif turno == "C":
            n = msg[i]
            byte = n.to_bytes(1, "little")
            parte_C += byte
            turno = "A"
    if largo_mensaje > 0:
        primer_byte_A = parte_A[0]
    else:
        primer_byte_A = 0
    if largo_mensaje >= 2:
        if len(parte_B) % 2 == 0:
            posicion_1 = int((len(parte_B) / 2) - 1)
            posicion_2 = int((len(parte_B) / 2))
            suma_centrales_B = parte_B[posicion_1] + parte_B[posicion_2]
        else:
            posicion = math.trunc(len(parte_B) / 2)
            suma_centrales_B = parte_B[posicion]
    else:
        suma_centrales_B = 0
    if largo_mensaje >= 3:
        ultimo_byte_C = parte_C[-1]
    else:
        ultimo_byte_C = 0
    suma_bytes = primer_byte_A + suma_centrales_B + ultimo_byte_C
    if suma_bytes % 2 == 0:
        n = 0
        byte_n = n.to_bytes(1, "little")
        return bytearray(byte_n + parte_C + parte_A + parte_B)
    else:
        n = 1
        byte_n = n.to_bytes(1, "little")
        return bytearray(byte_n + parte_A + parte_C + parte_B)


def desencriptar(msg: bytearray) -> bytearray:
    mensaje = msg[1:]
    msg_desencriptado = bytearray()
    if len(mensaje) % 3 == 0:
        largo_A = len(mensaje) // 3
        largo_B = len(mensaje) // 3
        largo_C = len(mensaje) // 3
    elif len(mensaje) % 3 == 1:
        largo_A = (len(mensaje) + 2) // 3
        largo_B = (len(mensaje) - largo_A) // 2
        largo_C = len(mensaje) - (largo_A + largo_B)
    elif len(mensaje) % 3 == 2:
        largo_A = (len(mensaje) + 1) // 3
        largo_B = (len(mensaje) + 1) // 3
        largo_C = len(mensaje) - (largo_A + largo_B)
    if msg[0] == 0:
        parte_C = mensaje[:largo_C]
        parte_A = mensaje[largo_C:(largo_C + largo_A)]
        parte_B = mensaje[-largo_B:]
    elif msg[0] == 1:
        parte_A = mensaje[:largo_A]
        parte_C = mensaje[largo_A:(largo_A + largo_C)]
        parte_B = mensaje[-largo_B:]
    if len(mensaje) % 3 == 0:
        turno = "C"
    elif len(mensaje) % 3 == 1:
        turno = "A"
    elif len(mensaje) % 3 == 2:
        turno = "B"
    for _ in range(len(mensaje)):
        if turno == "A":
            n = parte_A.pop()
            byte = n.to_bytes(1, "little")
            turno = "C"
        elif turno == "B":
            n = parte_B.pop()
            byte = n.to_bytes(1, "little")
            turno = "A"
        elif turno == "C":
            n = parte_C.pop()
            byte = n.to_bytes(1, "little")
            turno = "B"
        msg_desencriptado += byte
    return msg_desencriptado[::-1]


if __name__ == "__main__":
    # Testear encriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')

    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")

    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
