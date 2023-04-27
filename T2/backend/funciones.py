import backend.parametros as p
from random import choice, randint
from PyQt5.QtCore import QRect


def seleccionar_ruta_zombie(tipo, estado):
    if tipo == "walker" and estado == 1:
        return p.RUTA_WALKER_CAMINANDO_1
    elif tipo == "walker" and estado == 2:
        return p.RUTA_WALKER_CAMINANDO_2
    elif tipo == "walker" and estado == 3:
        return p.RUTA_WALKER_COMIENDO_1
    elif tipo == "walker" and estado == 4:
        return p.RUTA_WALKER_COMIENDO_2
    elif tipo == "walker" and estado == 5:
        return p.RUTA_WALKER_COMIENDO_3
    if tipo == "runner" and estado == 1:
        return p.RUTA_RUNNER_CAMINANDO_1
    elif tipo == "runner" and estado == 2:
        return p.RUTA_RUNNER_CAMINANDO_2
    elif tipo == "runner" and estado == 3:
        return p.RUTA_RUNNER_COMIENDO_1
    elif tipo == "runner" and estado == 4:
        return p.RUTA_RUNNER_COMIENDO_2
    elif tipo == "runner" and estado == 5:
        return p.RUTA_RUNNER_COMIENDO_3


def seleccionar_ruta_planta(tipo, estado):
    if tipo == "clasica" and estado == 1:
        return p.RUTA_PLANTA_CLASICA_1
    elif tipo == "clasica" and estado == 2:
        return p.RUTA_PLANTA_CLASICA_2
    elif tipo == "clasica" and estado == 3:
        return p.RUTA_PLANTA_CLASICA_3
    elif tipo == "clasica" and estado == 4:
        return p.RUTA_PLANTA_CLASICA_2
    elif tipo == "azul" and estado == 1:
        return p.RUTA_PLANTA_AZUL_1
    elif tipo == "azul" and estado == 2:
        return p.RUTA_PLANTA_AZUL_2
    elif tipo == "azul" and estado == 3:
        return p.RUTA_PLANTA_AZUL_3
    elif tipo == "azul" and estado == 4:
        return p.RUTA_PLANTA_AZUL_2
    elif tipo == "girasol" and estado == 1:
        return p.RUTA_GIRASOL_1
    elif tipo == "girasol" and estado == 2:
        return p.RUTA_GIRASOL_2
    elif tipo == "patata" and estado == 1:
        return p.RUTA_PATATA_1
    elif tipo == "patata" and estado == 2:
        return p.RUTA_PATATA_2
    elif tipo == "patata" and estado == 3:
        return p.RUTA_PATATA_3


def seleccionar_ruta_guisante(tipo, estado):
    if tipo == "clasico" and estado == 1:
        return p.RUTA_GUISANTE_CLASICO_1
    elif tipo == "clasico" and estado == 2:
        return p.RUTA_GUISANTE_CLASICO_2
    elif tipo == "clasico" and estado == 3:
        return p.RUTA_GUISANTE_CLASICO_3
    elif tipo == "azul" and estado == 1:
        return p.RUTA_GUISANTE_AZUL_1
    elif tipo == "azul" and estado == 2:
        return p.RUTA_GUISANTE_AZUL_2
    elif tipo == "azul" and estado == 3:
        return p.RUTA_GUISANTE_AZUL_3


def elegir_fila_zombie(zombies_fila_1, zombies_fila_2):
    if zombies_fila_1 < p.N_ZOMBIES and zombies_fila_2 < p.N_ZOMBIES:
        fila = choice([1, 2])
    elif zombies_fila_1 == p.N_ZOMBIES and zombies_fila_2 < p.N_ZOMBIES:
        fila = 2
    elif zombies_fila_1 < p.N_ZOMBIES and zombies_fila_2 == p.N_ZOMBIES:
        fila = 1
    else:
        fila = 0
    return fila


def elegir_tipo_zombie():
    return choice(p.TIPO_ZOMBIE)


def geometry_gis(casilla):
    x = casilla.x[1]  # Final ancho casilla
    y = casilla.y[0]  # Principio alto casilla
    return QRect(x, y, p.ANCHO_GUISANTE, p.ALTO_GUISANTE)


def geometry_sol(tipo, casilla):
    if tipo == "escenario":
        x = randint(p.ANCHO_JARDIN[0], p.ANCHO_JARDIN[1])
        y = randint(p.ALTO_JARDIN[0], p.ALTO_JARDIN[1])
    elif tipo == "planta":
        ancho_casilla = casilla.x
        alto_casilla = casilla.y
        x = randint(ancho_casilla[0] + 5, ancho_casilla[1] + 5)
        y = randint(alto_casilla[0] + 5, alto_casilla[1] + 5)
    return QRect(x, y, p.ANCHO_SOL, p.ALTO_SOL)


def soles(escenario):
    if escenario == "diurno":
        soles = p.SOLES_POR_RECOLECCION * 2
    elif escenario == "nocturno":
        soles = p.SOLES_POR_RECOLECCION
    return soles


def puntaje(escenario):
    if escenario == "diurno":
        puntaje = p.PUNTAJE_ZOMBIE_DIURNO
    elif escenario == "nocturno":
        puntaje = p.PUNTAJE_ZOMBIE_NOCTURNO
    return puntaje


def ruta_deteriorar(planta):
    if planta.vida >= 12:
        ruta = seleccionar_ruta_planta(planta.tipo, 1)
    elif planta.vida >= 6 and planta.vida < 12:
        ruta = seleccionar_ruta_planta(planta.tipo, 2)
    elif planta.vida > 0 and planta.vida < 6:
        ruta = seleccionar_ruta_planta(planta.tipo, 3)
    return ruta


def calcular_ptotal(puntaje, ponderador, estado_ronda):
    if estado_ronda == "ganada":
        puntaje_extra = round(puntaje * ponderador)  # Se redondea para poder ordenar ranking
        puntaje_final = puntaje + puntaje_extra
    elif estado_ronda == "perdida":
        puntaje_final = puntaje
    return puntaje_final
