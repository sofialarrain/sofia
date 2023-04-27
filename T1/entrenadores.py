from random import random, choice


class Entrenador:

    def __init__(self, nombre, programones, energia, objetos):
        self.nombre = nombre
        self.programones = programones
        self.__energia = energia
        self.objetos = objetos

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, valor):
        if valor < 0:
            self.__energia = 0
        elif valor > 100:
            self.__energia = 100
        else:
            self.__energia = valor

    def estado_entrenador(self):

        objetos_entrenador = []
        for objeto in self.objetos:
            objetos_entrenador.append(objeto.nombre)
        objetos_entrenador = ", ".join(objetos_entrenador)

        print("-" * 50)
        print("{: ^50}".format("*** Estado entrenador ***"))
        print("-" * 50)
        print(f"Nombre: {self.nombre}")
        print(f"Energía: {self.energia}")
        print(f"Objetos: {objetos_entrenador}")
        print("-" * 50)
        print("{: ^50}".format("Programones"))
        print("-" * 50)
        print("NOMBRE                | TIPO   |   NIVEL|    VIDA")

        for p in self.programones:
            print(f"{p.nombre:21s} | {p.tipo:6s} | {p.nivel: 6d} | {p.vida: 6d}")
        print()

    def crear_objetos(self, objeto, objetos_disponibles):
        e_inicial = self.energia
        if objeto == "baya":
            baya = choice(objetos_disponibles["Baya"])
            if self.energia >= baya.costo:
                self.energia -= baya.costo
                print(f"La energía de tu entrenador a disminuido de {e_inicial} a {self.energia}.")
                if random() < baya.probabilidad_exito:
                    self.objetos.append(baya)
                    print(f"El objeto <{baya.nombre}> del tipo <Baya> se ha creado con éxito.\n")
                else:
                    print("No se ha logrado crear un objeto del tipo <Baya>.\n")
            else:
                print("Tu entrenador no tiene la suficiente energía para un crear un objeto.\n")

        elif objeto == "pocion":
            pocion = choice(objetos_disponibles["Poción"])
            if self.energia >= pocion.costo:
                self.energia -= pocion.costo
                print(f"La energía de tu entrenador a disminuido de {e_inicial} a {self.energia}.")
                if random() < pocion.probabilidad_exito:
                    self.objetos.append(pocion)
                    print(f"El objeto {pocion.nombre} del tipo <Poción> se ha creado con éxito.\n")
                else:
                    print("No se ha logrado crear un objeto del tipo <Poción>.\n")
            else:
                print("Tu entrenador no tiene la suficiente energía para un crear un objeto.\n")

        elif objeto == "caramelo":
            caramelo = choice(objetos_disponibles["Caramelo"])
            if self.energia >= caramelo.costo:
                self.energia -= caramelo.costo
                print(f"La energía de tu entrenador a disminuido de {e_inicial} a {self.energia}.")
                if random() < caramelo.probabilidad_exito:
                    self.objetos.append(caramelo)
                    print(f"El objeto {caramelo.nombre} del tipo <Caramelo> se ha \
                        creado con éxito.\n")
                else:
                    print("No se ha logrado crear un objeto del tipo <Caramelo>.\n")
            else:
                print("Tu entrenador no tiene la suficiente energía para un crear un objeto.\n")

    def utilizar_objetos(self, objeto, programon):
        print(f"Programón beneficiado: {programon.nombre}")
        print(f"Objeto utilizado: {objeto.nombre} (Tipo {objeto.tipo})")
        objeto.aplicar_objeto(programon)
        posicion_objeto = self.objetos.index(objeto)
        self.objetos.pop(posicion_objeto)
        print()
