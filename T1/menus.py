from parametros import ENERGIA_ENTRENAMIENTO
from liga_programon import LigaProgramon
from sys import exit


def menu_inicio(campeonato):

    print("-" * 76)
    print("{: ^76s}".format("*** Menu de Inicio ***"))
    print("-" * 76)
    print("Eliga un entrenador:")
    for i in range(len(campeonato.entrenadores)):
        programones = []
        for programon in campeonato.entrenadores[i].programones:
            programones.append(programon.nombre)
        programones = ", ".join(programones)
        print(f"[{i + 1}] {campeonato.entrenadores[i].nombre}: {programones}")

    numero_salir = len(campeonato.entrenadores) + 1
    print(f"[{numero_salir}] Salir\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):
        if int(opcion_elegida) >= 1 and int(opcion_elegida) <= len(campeonato.entrenadores):
            campeonato.entrenador = campeonato.entrenadores[int(opcion_elegida) - 1]
            print(f"Has escogido a {campeonato.entrenador.nombre} como tu entrenador.\n")
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == numero_salir:
            return salir()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return menu_inicio(campeonato)

    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return menu_inicio(campeonato)


def menu_entrenador(campeonato):
    entrenador = campeonato.entrenador
    print("-" * 26)
    print("{: ^26s}".format("*** Menú Entrenador ***"))
    print("-" * 26)
    print("[1] Entrenamiento")
    print("[2] Simular ronda")
    print("[3] Resumen campeonato")
    print("[4] Crear objetos")
    print("[5] Utilizar objetos")
    print("[6] Estado entrenador")
    print("[7] Volver Menu de Inicio")
    print("[8] Salir campeonato\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):

        if int(opcion_elegida) == 1:
            if entrenador.energia < 20:
                print("Tu entrenador no tiene la suficiente energía para un entrenamiento.\n")
                return menu_entrenador(campeonato)
            else:
                return menu_entrenamiento(campeonato)

        elif int(opcion_elegida) == 2:
            elegir_luchador(entrenador, campeonato)

        elif int(opcion_elegida) == 3:
            campeonato.resumen_campeonato()
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == 4:
            objetos_disponibles = campeonato.objetos_disponibles
            elegir_objeto_para_crear(entrenador, objetos_disponibles, campeonato)
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == 5:
            if len(entrenador.objetos) > 0:
                elegir_objeto_para_utilizar(entrenador, campeonato)
            else:
                print("Lo siento. Tu entrenador no tiene objetos.\n")
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == 6:
            entrenador.estado_entrenador()
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == 7:
            return menu_inicio(campeonato)

        elif int(opcion_elegida) == 8:
            return salir()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return menu_entrenador(campeonato)

    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return menu_entrenador(campeonato)


def menu_entrenamiento(campeonato):
    entrenador = campeonato.entrenador
    print("-" * 40)
    print("{: ^40s}".format("*** Menú de entrenamiento ***"))
    print("-" * 40)
    print("Eliga el programón que desea entrenar:")
    for i in range(len(entrenador.programones)):
        programon = entrenador.programones[i]
        print(f"[{i + 1}] {programon.nombre}")

    numero_volver = len(entrenador.programones) + 1
    numero_salir = len(entrenador.programones) + 2
    print(f"[{numero_volver}] Volver")
    print(f"[{numero_salir}] Salir campeonato\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):

        if int(opcion_elegida) >= 1 and int(opcion_elegida) <= len(entrenador.programones):
            energia_inicial = entrenador.energia
            entrenador.energia -= ENERGIA_ENTRENAMIENTO
            programon = entrenador.programones[int(opcion_elegida) - 1]
            programon.entrenamiento()
            print(f"Has gastado {ENERGIA_ENTRENAMIENTO} de energía.")
            print(f"Tú energía a disminuido de {energia_inicial} a {entrenador.energia}.\n")
            if programon.nivel >= programon.nivel_megaevolucion and not programon.evolucionado:
                programon.mega_evolucionar()
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == numero_volver:
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == numero_salir:
            return salir()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return menu_entrenamiento(campeonato)

    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return menu_entrenamiento(campeonato)


def elegir_luchador(entrenador, campeonato):
    print("{: ^26s}".format("*** Elige tu luchador ***"))
    print("-" * 26)
    for i in range(len(entrenador.programones)):
        programon = entrenador.programones[i]
        print(f"[{i + 1}] {programon.nombre}")

    numero_volver = len(entrenador.programones) + 1
    numero_salir = len(entrenador.programones) + 2
    print(f"[{numero_volver}] Volver")
    print(f"[{numero_salir}] Salir\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):

        if int(opcion_elegida) >= 1 and int(opcion_elegida) <= len(entrenador.programones):
            programon = entrenador.programones[int(opcion_elegida) - 1]
            resultado = campeonato.simunar_ronda(programon)
            if resultado == "seguir":
                return menu_entrenador(campeonato)
            elif resultado == "fin campeonato":
                return fin_campeonato(campeonato)

        elif int(opcion_elegida) == numero_volver:
            return menu_entrenador(campeonato)

        elif int(opcion_elegida) == numero_salir:
            return salir()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return elegir_luchador(entrenador, campeonato)
    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return elegir_luchador(entrenador, campeonato)


def elegir_objeto_para_crear(entrenador, objetos_disponibles, campeonato):
    print("-" * 26)
    print("{: ^26}".format("*** Menú Objetos ***"))
    print("-" * 26)
    print("[1] Baya")
    print("[2] Poción")
    print("[3] Caramelo")
    print("[4] Volver")
    print("[5] Salir")
    print()

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):
        if int(opcion_elegida) == 1:
            entrenador.crear_objetos("baya", objetos_disponibles)
            return menu_entrenador(campeonato)
        elif int(opcion_elegida) == 2:
            entrenador.crear_objetos("pocion", objetos_disponibles)
            return menu_entrenador(campeonato)
        elif int(opcion_elegida) == 3:
            entrenador.crear_objetos("caramelo", objetos_disponibles)
            return menu_entrenador(campeonato)
        elif int(opcion_elegida) == 4:
            return menu_entrenador(campeonato)
        elif int(opcion_elegida) == 5:
            return salir()
        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return elegir_objeto_para_crear(entrenador, objetos_disponibles, campeonato)
    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return elegir_objeto_para_crear(entrenador, objetos_disponibles, campeonato)


def elegir_objeto_para_utilizar(entrenador, campeonato):
    print("-" * 30)
    print("{: ^30}".format("*** Objetos disponibles ***"))
    print("-" * 30)

    for i in range(len(entrenador.objetos)):
        objeto = entrenador.objetos[i]
        print(f"[{i + 1}] {objeto.nombre}")

    numero_volver = len(entrenador.objetos) + 1
    numero_salir = len(entrenador.objetos) + 2
    print(f"[{numero_volver}] Volver")
    print(f"[{numero_salir}] Salir\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):

        if int(opcion_elegida) >= 1 and int(opcion_elegida) <= len(entrenador.objetos):
            objeto = entrenador.objetos[int(opcion_elegida) - 1]

            print("Escoga el programón donde se aplicará el objeto:")
            for i in range(len(entrenador.programones)):
                programon = entrenador.programones[i]
                print(f"[{i + 1}] {programon.nombre}")

            numero_volver = len(entrenador.programones) + 1
            numero_salir = len(entrenador.programones) + 2

            print(f"[{numero_volver}] Volver")
            print(f"[{numero_salir}] Salir")
            print()

            opcion_elegida = input("Ingrese una opción: ")
            print()

            if (opcion_elegida.isdigit()):
                if int(opcion_elegida) >= 1 and int(opcion_elegida) <= len(entrenador.programones):
                    programon = entrenador.programones[int(opcion_elegida) - 1]
                    entrenador.utilizar_objetos(objeto, programon)
                    return menu_entrenador(campeonato)

                elif int(opcion_elegida) == numero_volver:
                    return menu_entrenador(campeonato)

                elif int(opcion_elegida) == numero_salir:
                    return menu_inicio(campeonato)

                else:
                    print("Error. Solo puede ingresar números que se encuentren en las opciones.")
                    elegir_objeto_para_utilizar(entrenador, campeonato)

            elif int(opcion_elegida) == numero_volver:
                return menu_entrenador(campeonato)

            elif int(opcion_elegida) == numero_salir:
                return menu_inicio(campeonato)
            else:
                print("Error. Solo puede ingresar números que se encuentren en las opciones.")
                return elegir_objeto_para_utilizar(entrenador, campeonato)

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.")
            return elegir_objeto_para_utilizar(entrenador, campeonato)

    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.")
        return elegir_objeto_para_utilizar(entrenador, campeonato)


def salir():
    print("Saliendo del DCCampeonato Programón...")
    return exit()


def fin_campeonato(campeonato):
    print()
    print("#" * 70)
    print("{: ^70s}".format("FIN DCCAMPEONATO PROGRAMÓN"))
    print("#" * 70)
    print()
    return inicio_o_salir(campeonato)


def inicio_o_salir(campeonato):
    print("-" * 23)
    print("Seleccione una opción:")
    print("[1] Menu Inicio")
    print("[2] Salir campeonato\n")

    opcion_elegida = input("Ingrese una opción: ")
    print()

    if (opcion_elegida.isdigit()):
        if int(opcion_elegida) == 1:
            return comenzar_otro_campeonato(campeonato)
        elif int(opcion_elegida) == 2:
            return salir()
        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
            return inicio_o_salir(campeonato)
    else:
        print("Error. Solo puede ingresar números que se encuentren en las opciones.\n")
        return inicio_o_salir(campeonato)


def comenzar_otro_campeonato(campeonato):
    programones = campeonato.programones
    entrenadores = campeonato.entrenadores
    objetos = campeonato.objetos
    objetos_disponibles = campeonato.objetos_disponibles
    campeonato = LigaProgramon(programones, entrenadores, objetos, objetos_disponibles)
    return menu_inicio(campeonato)
