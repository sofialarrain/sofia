from parametros import MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO, \
    AUMENTAR_VIDA_PLANTA, AUMENTAR_ATAQUE_FUEGO, AUMENTAR_VELOCIDAD_AGUA, \
    MEGA_VIDA, MEGA_ATAQUE, MEGA_DEFENSA, MEGA_VELOCIDAD
from random import randint
from abc import ABC, abstractmethod


class Programon(ABC):

    def __init__(self, nombre, tipo, nivel, vida, ataque, defensa, velocidad, mega_evolucion):
        self.nombre = nombre
        self.tipo = tipo
        self.__nivel = nivel
        self.__vida = vida
        self.__ataque = ataque
        self.__defensa = defensa
        self.__velocidad = velocidad
        self.__experiencia = 0
        self.nivel_megaevolucion = mega_evolucion[0]
        self.mega_evolucion = mega_evolucion[1]
        self.evolucionado = mega_evolucion[2]

    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, valor):
        if valor < 1:
            self.__nivel = 1
        elif valor > 100:
            self.__nivel = 100
        else:
            self.__nivel = valor

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, valor):
        if valor < 1:
            self.__vida = 1
        elif valor > 255:
            self.__vida = 255
        else:
            self.__vida = valor

    @property
    def ataque(self):
        return self.__ataque

    @ataque.setter
    def ataque(self, valor):
        if valor < 5:
            self.__ataque = 5
        elif valor > 190:
            self.__ataque = 190
        else:
            self.__ataque = valor

    @property
    def defensa(self):
        return self.__defensa

    @defensa.setter
    def defensa(self, valor):
        if valor < 5:
            self.__defensa = 5
        elif valor > 250:
            self.__defensa = 250
        else:
            self.__defensa = valor

    @property
    def velocidad(self):
        return self.__velocidad

    @velocidad.setter
    def velocidad(self, valor):
        if valor < 5:
            self.__velocidad = 5
        elif valor > 200:
            self.__velocidad = 200
        else:
            self.__velocidad = valor

    @property
    def experiencia(self):
        return self.__experiencia

    @experiencia.setter
    def experiencia(self, valor):
        if valor < 0:
            self.__experiencia = 0
        elif valor >= 100:
            self.nivel += 1
            self.__experiencia = (valor - 100)
            self.vida += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO)
            self.ataque += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO)
            self.defensa += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO)
            self.velocidad += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO)
        else:
            self.__experiencia = valor

    def entrenamiento(self):
        exp_inicial = self.experiencia
        nivel_inicial = self.nivel
        self.experiencia += randint(MIN_AUMENTO_ENTRENAMIENTO, MAX_AUMENTO_ENTRENAMIENTO)
        print(f"Entrenando a {self.nombre}.")
        print(f"La experiencia de tu programón a cambiado de {exp_inicial} a {self.experiencia}.")
        if nivel_inicial != self.nivel:
            print(f"{self.nombre} ha subido de nivel {nivel_inicial} a nivel {self.nivel}.")

    def luchar(self, rival):
        puntaje_victoria = max(
                                0, (self.vida * 0.2 + self.nivel * 0.3 + self.ataque * 0.15
                                    + self.defensa * 0.15 + self.velocidad * 0.2
                                    + self.ventaja(rival) * 40))
        return puntaje_victoria

    @abstractmethod
    def ganar_batalla(self):
        pass

    @abstractmethod
    def ventaja(self):
        pass

    def mega_evolucionar(self):
        programon_sin_evolucionar = self.nombre
        self.nombre = self.mega_evolucion
        self.vida += MEGA_VIDA
        self.ataque += MEGA_ATAQUE
        self.defensa += MEGA_DEFENSA
        self.velocidad += MEGA_VELOCIDAD
        self.evolucionado = True
        print("*" * 60)
        print(f"Programón a evolucionado de {programon_sin_evolucionar} a {self.nombre}.")
        print(f"Vida ha aumentado de {self.vida - MEGA_VIDA} a {self.vida}.")
        print(f"Ataque ha aumentado de {self.ataque - MEGA_ATAQUE} a {self.ataque}.")
        print(f"Defensa ha aumentado de {self.defensa - MEGA_DEFENSA} a {self.defensa}.")
        print(f"Velocidad ha aumentado de {self.velocidad - MEGA_VELOCIDAD} a {self.velocidad}.")
        print("*" * 60)
        print()


class TipoPlanta(Programon):

    def __init__(self, *args):
        super().__init__(*args)

    def ganar_batalla(self):
        self.vida += AUMENTAR_VIDA_PLANTA

    def ventaja(self, rival):
        if rival.tipo == "planta":
            ventaja = 0
        elif rival.tipo == "fuego":
            ventaja = -1
        elif rival.tipo == "agua":
            ventaja = 1
        return ventaja


class TipoFuego(Programon):

    def __init__(self, *args):
        super().__init__(*args)

    def ganar_batalla(self):
        self.ataque += AUMENTAR_ATAQUE_FUEGO

    def ventaja(self, rival):
        if rival.tipo == "planta":
            ventaja = 1
        elif rival.tipo == "fuego":
            ventaja = 0
        elif rival.tipo == "agua":
            ventaja = -1
        return ventaja


class TipoAgua(Programon):

    def __init__(self, *args):
        super().__init__(*args)

    def ganar_batalla(self):
        self.vida += AUMENTAR_VELOCIDAD_AGUA

    def ventaja(self, rival):
        if rival.tipo == "planta":
            ventaja = -1
        elif rival.tipo == "fuego":
            ventaja = 1
        elif rival.tipo == "agua":
            ventaja = 0
        return ventaja
