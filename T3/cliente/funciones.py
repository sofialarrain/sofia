import json
import os.path


def valor_parametro(llave):
    ruta = os.path.join("parametros.json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        diccionario = json.load(archivo)
    valor = diccionario[llave]
    return valor


def seleccionar_ruta_carta(carta):
    if carta is not None:
        elemento = carta["elemento"]
        color = carta["color"]
        puntos = int(carta["puntos"])
        if color == "azul":
            if elemento == "agua":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_AZUL_AGUA_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_AZUL_AGUA_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_AZUL_AGUA_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_AZUL_AGUA_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_AZUL_AGUA_5"))
            elif elemento == "fuego":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_AZUL_FUEGO_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_AZUL_FUEGO_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_AZUL_FUEGO_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_AZUL_FUEGO_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_AZUL_FUEGO_5"))
            elif elemento == "nieve":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_AZUL_NIEVE_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_AZUL_NIEVE_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_AZUL_NIEVE_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_AZUL_NIEVE_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_AZUL_NIEVE_5"))
        elif color == "rojo":
            if elemento == "agua":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_ROJO_AGUA_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_ROJO_AGUA_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_ROJO_AGUA_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_ROJO_AGUA_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_ROJO_AGUA_5"))
            elif elemento == "fuego":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_ROJO_FUEGO_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_ROJO_FUEGO_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_ROJO_FUEGO_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_ROJO_FUEGO_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_ROJO_FUEGO_5"))
            elif elemento == "nieve":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_ROJO_NIEVE_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_ROJO_NIEVE_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_ROJO_NIEVE_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_ROJO_NIEVE_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_ROJO_NIEVE_5"))
        elif color == "verde":
            if elemento == "agua":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_VERDE_AGUA_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_VERDE_AGUA_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_VERDE_AGUA_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_VERDE_AGUA_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_VERDE_AGUA_5"))
            elif elemento == "fuego":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_VERDE_FUEGO_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_VERDE_FUEGO_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_VERDE_FUEGO_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_VERDE_FUEGO_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_VERDE_FUEGO_5"))
            elif elemento == "nieve":
                if puntos == 1:
                    return os.path.join(*valor_parametro("RUTA_VERDE_NIEVE_1"))
                elif puntos == 2:
                    return os.path.join(*valor_parametro("RUTA_VERDE_NIEVE_2"))
                elif puntos == 3:
                    return os.path.join(*valor_parametro("RUTA_VERDE_NIEVE_3"))
                elif puntos == 4:
                    return os.path.join(*valor_parametro("RUTA_VERDE_NIEVE_4"))
                elif puntos == 5:
                    return os.path.join(*valor_parametro("RUTA_VERDE_NIEVE_5"))
    else:
        return None


def seleccionar_ruta_ficha(carta):
    if carta is not None:
        elemento = carta["elemento"]
        color = carta["color"]
        if elemento == "agua":
            if color == "azul":
                return os.path.join(*valor_parametro("RUTA_AGUA_AZUL"))
            elif color == "rojo":
                return os.path.join(*valor_parametro("RUTA_AGUA_ROJO"))
            elif color == "verde":
                return os.path.join(*valor_parametro("RUTA_AGUA_VERDE"))
        elif elemento == "fuego":
            if color == "azul":
                return os.path.join(*valor_parametro("RUTA_FUEGO_AZUL"))
            elif color == "rojo":
                return os.path.join(*valor_parametro("RUTA_FUEGO_ROJO"))
            elif color == "verde":
                return os.path.join(*valor_parametro("RUTA_FUEGO_VERDE"))
        elif elemento == "nieve":
            if color == "azul":
                return os.path.join(*valor_parametro("RUTA_NIEVE_AZUL"))
            elif color == "rojo":
                return os.path.join(*valor_parametro("RUTA_NIEVE_ROJO"))
            elif color == "verde":
                return os.path.join(*valor_parametro("RUTA_NIEVE_VERDE"))
    else:
        return None
