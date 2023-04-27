from liga_programon import LigaProgramon
from programones import TipoPlanta, TipoFuego, TipoAgua
from entrenadores import Entrenador
from objetos import Baya, Pocion, Caramelo
from parametros import MEGA_VIDA, MEGA_ATAQUE, MEGA_DEFENSA, MEGA_VELOCIDAD
import menus


lista_programones = []
lista_entrenadores = []
lista_objetos = []
objetos_disp = {"Baya": [], "Poción": [], "Caramelo": []}
evoluciones = {}


def mega_evolucion_inicial(programon):
    programon.nombre = programon.mega_evolucion
    programon.vida += MEGA_VIDA
    programon.ataque += MEGA_ATAQUE
    programon.defensa += MEGA_DEFENSA
    programon.velocidad += MEGA_VELOCIDAD
    programon.evolucionado = True


# Cargar datos
with open("evoluciones.csv", "rt", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    atributos = lineas[0].strip("\n").split(",")
    columna = -1
    # CVS dinámico
    for i in range(3):
        columna += 1
        if atributos[i] == "nombre":
            nombre = columna
        elif atributos[i] == "nivel":
            nivel = columna
        elif atributos[i] == "evolucion":
            evolucion = columna
    for i in range(1, len(lineas)):
        linea = lineas[i].strip("\n").split(",")
        nombre_programon = linea[nombre]
        nivel_programon = int(linea[nivel])
        evolucion_programon = linea[evolucion]
        evolucionado = False
        evoluciones[f"{nombre_programon}"] = (nivel_programon, evolucion_programon, evolucionado)


with open("programones.csv", "rt", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    atributos = lineas[0].strip("\n").split(",")
    columna = -1
    # CVS dinámico
    for i in range(7):
        columna += 1
        if atributos[i] == "nombre":
            columna_nombre = columna
        elif atributos[i] == "tipo":
            columna_tipo = columna
        elif atributos[i] == "nivel":
            columna_nivel = columna
        elif atributos[i] == "vida":
            columna_vida = columna
        elif atributos[i] == "ataque":
            columna_ataque = columna
        elif atributos[i] == "defensa":
            columna_defensa = columna
        elif atributos[i] == "velocidad":
            columna_velocidad = columna
    for i in range(1, len(lineas)):
        linea = lineas[i].strip("\n").split(",")
        nombre = linea[columna_nombre]
        tipo = linea[columna_tipo]
        nivel = int(linea[columna_nivel])
        vida = int(linea[columna_vida])
        ataque = int(linea[columna_ataque])
        defensa = int(linea[columna_defensa])
        velocidad = int(linea[columna_velocidad])
        mega_ev = evoluciones[f"{nombre}"]
        if tipo == "planta":
            programon = TipoPlanta(nombre, tipo, nivel, vida, ataque, defensa, velocidad, mega_ev)
        elif tipo == "fuego":
            programon = TipoFuego(nombre, tipo, nivel, vida, ataque, defensa, velocidad, mega_ev)
        elif tipo == "agua":
            programon = TipoAgua(nombre, tipo, nivel, vida, ataque, defensa, velocidad, mega_ev)
        if nivel >= mega_ev[0]:
            mega_evolucion_inicial(programon)
        lista_programones.append(programon)

with open("objetos.csv", "rt", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    atributos = lineas[0].strip("\n").split(",")
    columna = -1
    # CVS dinámico
    for i in range(2):
        columna += 1
        if atributos[i] == "nombre":
            columna_nombre = columna
        elif atributos[i] == "tipo":
            columna_tipo = columna
    for i in range(1, len(lineas)):
        linea = lineas[i].strip("\n").split(",")
        nombre = linea[columna_nombre]
        tipo = linea[columna_tipo]
        if tipo == "baya":
            objeto = Baya(nombre, tipo)
            objetos_disp["Baya"].append(objeto)
        elif tipo == "pocion":
            objeto = Pocion(nombre, tipo)
            objetos_disp["Poción"].append(objeto)
        elif tipo == "caramelo":
            objeto = Caramelo(nombre, tipo)
            objetos_disp["Caramelo"].append(objeto)
        lista_objetos.append(objeto)

with open("entrenadores.csv", "rt", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    atributos = lineas[0].strip("\n").split(",")
    columna = -1
    # CVS dinámico
    for i in range(4):
        columna += 1
        if atributos[i] == "nombre":
            columna_nombre = columna
        elif atributos[i] == "programones":
            columna_programones = columna
        elif atributos[i] == "energia":
            columna_energia = columna
        elif atributos[i] == "objetos":
            columna_objetos = columna

    for i in range(1, len(lineas)):
        linea = lineas[i].strip("\n").split(",")
        nombre = linea[columna_nombre]
        energia = int(linea[columna_energia])

        # Buscar objetos Programon con nombres de los programones
        nombres_programones_entrenador = linea[columna_programones].split(";")
        programones_entrenador = []
        for programon in lista_programones:
            if programon.nombre in nombres_programones_entrenador:
                programones_entrenador.append(programon)

        # Buscar objetos Objeto con nombres de los objetos
        nombres_objetos_entrenador = linea[columna_objetos].split(";")
        objetos_entrenador = []
        for objeto in lista_objetos:
            if objeto.nombre in nombres_objetos_entrenador:
                objetos_entrenador.append(objeto)
        entrenador = Entrenador(nombre, programones_entrenador, energia, objetos_entrenador)
        lista_entrenadores.append(entrenador)

campeonato = LigaProgramon(lista_programones, lista_entrenadores, lista_objetos, objetos_disp)
menus.menu_inicio(campeonato)
