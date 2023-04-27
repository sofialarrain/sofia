from random import choice


class LigaProgramon:

    def __init__(self, programones, entrenadores, objetos, objetos_disponibles):
        self.programones = programones  # Todos los programones posibles
        self.entrenadores = entrenadores  # Todos los entrenadores posibles
        self.objetos = objetos  # Todos los objetos posibles
        self.objetos_disponibles = objetos_disponibles  # Tbjetos clasificados por tipo
        self.entrenador = ""
        self.entrenadores_jugando = entrenadores
        self.perdedores = []
        self.ronda_actual = 1
        self.campeon = ""

    def simunar_ronda(self, programon):

        print("{: ^70s}".format(f"Ronda {self.ronda_actual}"))
        print("-" * 70)

        # Crear parejas ronda
        parejas = []
        sin_pareja = self.entrenadores_jugando.copy()
        posicion_entrenador = sin_pareja.index(self.entrenador)
        sin_pareja.pop(posicion_entrenador)
        rival = choice(sin_pareja)
        posicion_rival = sin_pareja.index(rival)
        sin_pareja.pop(posicion_rival)
        programon_rival = choice(rival.programones)
        pareja = [[self.entrenador, programon], [rival, programon_rival]]
        parejas.append(pareja)

        while len(sin_pareja) > 0:
            rival_1 = choice(sin_pareja)
            posicion_rival_1 = sin_pareja.index(rival_1)
            sin_pareja.pop(posicion_rival_1)
            rival_2 = choice(sin_pareja)
            posicion_rival_2 = sin_pareja.index(rival_2)
            sin_pareja.pop(posicion_rival_2)
            programon_1 = choice(rival_1.programones)
            programon_2 = choice(rival_2.programones)
            pareja = ([rival_1, programon_1], [rival_2, programon_2])
            parejas.append(pareja)

        # Enfrentar parejas
        entrenadores_invictos = []
        for pareja in parejas:
            rival_1 = pareja[0][0]
            rival_2 = pareja[1][0]
            programon_1 = pareja[0][1]
            programon_2 = pareja[1][1]
            print(f"{rival_1.nombre} usando al programón {programon_1.nombre}, se enfrenta a")
            print(f"{rival_2.nombre} usando al programón {programon_2.nombre}.")

            if programon_1.luchar(programon_2) >= programon_2.luchar(programon_1):
                entrenadores_invictos.append(rival_1)
                self.perdedores.append(rival_2.nombre)
                print(f"{rival_1.nombre} ha ganado la batalla.")
                programon_1.ganar_batalla()
                if rival_2 == self.entrenador:
                    print("-" * 70)
                    print(f"Tu entrenador {self.entrenador.nombre} a perdido la batalla. :(")
                    return "fin campeonato"

            else:
                entrenadores_invictos.append(rival_2)
                self.perdedores.append(rival_1.nombre)
                print(f"{rival_2.nombre} ha ganado la batalla.")
                programon_2.ganar_batalla()
                if rival_1 == self.entrenador:
                    print("-" * 70)
                    print(f"Tu entrenador {self.entrenador.nombre} a perdido la batalla. :(")
                    return "fin campeonato"

            rival_1.energia = 100
            rival_2.energia = 100
            self.entrenadores_jugando = entrenadores_invictos.copy()
            print()

        if self.ronda_actual == 4:
            # Solo se vera esto si gana el entrenador escogido
            # Si el entrenador pierde en alguna ronda se termina el campeonato para el jugador
            self.campeon = entrenadores_invictos[0]
            print("-" * 70)
            print(f"Felicitaciones tu entrenador {self.campeon.nombre} ha ganado el DCCampeonato.")
            print("-" * 70)
            return "fin campeonato"
        else:
            self.ronda_actual += 1
            return "seguir"

    def resumen_campeonato(self):
        participantes = []
        for entrenador in self.entrenadores:
            participantes.append(entrenador.nombre)
        participantes = ", ".join(participantes)

        entrenadores_jugando = []
        for entrenador in self.entrenadores_jugando:
            entrenadores_jugando.append(entrenador.nombre)
        entrenadores_jugando = ", ".join(entrenadores_jugando)

        perdedores = ", ".join(self.perdedores)

        print()
        print("{: ^177s}".format("Resumen Campeonato"))
        print("-" * 177)
        print(f"Participantes: {participantes}\n")
        print(f"Ronda actual: {self.ronda_actual}\n")
        print(f"Entrenadores que siguen en la competencia: {entrenadores_jugando}\n")
        print(f"Entrenadores derrotados: {perdedores}\n")
