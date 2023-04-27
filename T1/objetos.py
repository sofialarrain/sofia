from abc import ABC, abstractmethod
from parametros import AUMENTO_DEFENSA, GASTO_ENERGIA_BAYA, GASTO_ENERGIA_CARAMELO, GASTO_ENERGIA_POCION, \
    PROB_EXITO_CARAMELO, PROB_EXITO_POCION, PROB_EXITO_BAYA
from random import randint


class Objeto(ABC):

    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    @abstractmethod
    def aplicar_objeto(self, programon):
        pass


class Baya(Objeto):

    def __init__(self, *args):
        super().__init__(*args)
        self.costo = GASTO_ENERGIA_BAYA
        self.probabilidad_exito = PROB_EXITO_BAYA

    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        vida_inicial = programon.vida
        aumento_vida = randint(1, 10)
        programon.vida += aumento_vida
        print(f"Aumento vida: {aumento_vida}")
        print(f"La vida subió de {vida_inicial} a {programon.vida}.")


class Pocion(Objeto):

    def __init__(self, *args):
        super().__init__(*args)
        self.costo = GASTO_ENERGIA_POCION
        self.probabilidad_exito = PROB_EXITO_POCION

    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        ataque_inicial = programon.ataque
        aumento_ataque = randint(1, 7)
        programon.ataque += aumento_ataque
        print(f"Aumento ataque: {aumento_ataque}")
        print(f"El ataque subió de {ataque_inicial} a {programon.ataque}.")


class Caramelo(Baya, Pocion):

    def __init__(self, *args):
        super().__init__(*args)
        self.costo = GASTO_ENERGIA_CARAMELO
        self.probabilidad_exito = PROB_EXITO_CARAMELO

    def aplicar_objeto(self, programon):
        super().aplicar_objeto(programon)
        defensa_inical = programon.defensa
        programon.defensa += AUMENTO_DEFENSA
        print(f"Aumento defensa: {AUMENTO_DEFENSA}")
        print(f"La defensa subio de {defensa_inical} a {programon.defensa}.")
