from parametros import PROB_BESTIA
import math
import random
import os
import os.path
import sys
import juego


class MenuInicio:   

    def __init__(self):
        self.nombre_usuario = None
        self.nombre_archivo = ""  
        self.ancho_tablero = None
        self.largo_tablero = None
        self.cantidad_bestias = 0
        self.posiciones_bestias = []
        self.tablero = [] #tablero con bestias
        self.tablero2 = [] #tablero sin bestias
        self.casillas_descubiertas = 0
            

    def elegir_opciones(self):

        opcion_elegida = input(f"""
MENÚ DE INICIO

Seleccione una de las siguientes opciones:
[1] Crear una partida nueva
[2] Cargar una partida existente
[3] Visualizar ranking de puntajes
[4] Salir del programa 

Opción elegida: """)

        if (opcion_elegida.isdigit()):

            if int(opcion_elegida) == 1:
                self.crear_partida_nueva()

            elif int(opcion_elegida) == 2:
                self.cargar_partida_existente()
                
            elif int(opcion_elegida) == 3:
                self.ver_ranking()
            
            elif int(opcion_elegida) == 4:
                self.salir_programa()
            
            elif int(opcion_elegida) < 1 or int(opcion_elegida) > 4:
                print("Error. Solo puede ingresar números que se encuentren en las opciones.")
                self.elegir_opciones()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.")
            self.elegir_opciones()



    def crear_partida_nueva(self):

        self.nombre_usuario = input("\nIngrese un nombre de usuario: ")
        self.nombre_archivo = self.nombre_usuario + ".txt"

        #revisar si ya se creó carpeta "partidas"
        if os.path.exists("partidas"):

            #revisar si ya existe nombre de usuario
            path = os.path.join("partidas", self.nombre_archivo)  #path relativo
            if os.path.isfile(path): 
                print("Error. Este nombre de usuario ya esta registrado.")
                self.crear_partida_nueva()

        else:
            os.mkdir("partidas") 


        print("\nLas dimensiones del tablero deben ser de mínimo 3 x 3 y máximo 15 x 15.")

        #establecer ancho tablero
        ancho_correcto = False
        while not ancho_correcto:
            self.ancho_tablero = input("Eliga el ancho del tablero de jugada: ")

            if (self.ancho_tablero.isdigit()):
                if int(self.ancho_tablero) < 3 or int(self.ancho_tablero) > 15:
                    print("Error. El ancho del tablero debe ser de mínimo 3 y máximo 15 unidades.")
                
                else:
                    ancho = self.ancho_tablero
                    self.ancho_tablero = int(ancho)
                    ancho_correcto = True
            
            else:
                print("Error. Debe ingresar un número dentro de las dimensiones.") 
            
        #establecer largo tablero
        largo_correcto = False
        while not largo_correcto:
            self.largo_tablero = input("Eliga el largo del tablero de jugada: ")

            if (self.largo_tablero.isdigit()):
                if int(self.largo_tablero) < 3 or int(self.largo_tablero) > 15:
                    print("Error. El largo del tablero debe ser de mínimo 3 y máximo 15 unidades.")
                
                else:
                    largo = self.largo_tablero
                    self.largo_tablero = int(largo)
                    largo_correcto = True
            
            else:
                print("Error. Debe ingresar un número dentro de las dimensiones.")                
        
        print(f"\nMuy bien! El tablero de jugada será de {self.largo_tablero} x {self.ancho_tablero}.")


        #establecer posiciones de las bestias
        self.cantidad_bestias = int(math.ceil(self.ancho_tablero * self.largo_tablero * PROB_BESTIA))

        #no se repitan coordenadas
        bestias_posicionadas = False
        bestias_en_posicion = 0
        self.posiciones_bestias = []

        while not bestias_posicionadas:
            coordenada_x = random.randint(0, self.ancho_tablero - 1)
            coordenada_y = random.randint(0, self.largo_tablero - 1)
            coordenadas_bestia = [coordenada_y, coordenada_x]

            if coordenadas_bestia not in self.posiciones_bestias:
                self.posiciones_bestias.append(coordenadas_bestia)
                bestias_en_posicion += 1

                if bestias_en_posicion == self.cantidad_bestias:
                    bestias_posicionadas = True          


        #crear tablero bestias
        self.tablero = []
        for i in range(self.largo_tablero):
            fila = []
            for j in range(self.ancho_tablero):
                fila.append(" ")
            self.tablero.append(fila)

        #crear tablero sin bestias
        self.tablero2 = []
        for i in range(self.largo_tablero):
            fila2 = []
            for j in range(self.ancho_tablero):
                fila2.append(" ")
            self.tablero2.append(fila2)
        
        for posicion in self.posiciones_bestias:
            self.tablero[posicion[0]][posicion[1]] = "N"
                                 
        #escribir información en archivo
        path = os.path.join("partidas", self.nombre_archivo)

        with open(path, "wt", encoding="utf-8") as archivo:
            archivo.write(self.nombre_usuario + "\n" + str(self.ancho_tablero) + "\n" \
                + str(self.largo_tablero) + "\n" + str(self.cantidad_bestias) + "\n"  \
                    + str(self.tablero) + "\n" + str(self.tablero2) + "\n" \
                        + str(self.casillas_descubiertas) + "\n")

        print("\nCreando una nueva partida...")
        juego.MenuJuego.comenzar_juego(self, self.nombre_archivo)

   

    def cargar_partida_existente(self):

        self.nombre_usuario = input("\nIngrese su nombre de usuario: ")
        self.nombre_archivo = self.nombre_usuario + ".txt"

        #revisar si existe usuario registrado
        path = os.path.join("partidas", self.nombre_archivo)
        if os.path.isfile(path): 
            print(f"Reanudando partida a nombre del usuario <{self.nombre_usuario}>...")
            juego.MenuJuego.comenzar_juego(self, self.nombre_archivo)    
     
        else:
            print("Error. No existe una partida a nombre de este usuario.")
            self.elegir_opciones()



    def ver_ranking(self):

        #revisar si hay puntajes registrados
        if os.path.exists("puntajes.txt"):

            print("Los 10 puntajes más altos hasta el momento son:")
            
            #ordenar puntajes
            ranking = [] 
            with open("puntajes.txt", "rt", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
                for linea in lineas:
                    l = linea.split(":")
                    l[1] = int(l[1])
                    ranking.append(l)
                
            ranking.sort(key=lambda x: x[1], reverse=True)  

            cantidad_usuarios = len(ranking)

            if cantidad_usuarios < 10:
                for i in range(cantidad_usuarios):
                    print(f"[{i + 1}] {ranking[i][0]}: {ranking[i][1]}")
            
            else:
                for i in range(10):
                    print(f"[{i + 1}] {ranking[i][0]}: {ranking[i][1]}")
        
        else:
            print("Todavia no hay puntajes registrados.")

        self.inicio_o_salir()
        


    #función para elegir si ir a menu inicio o salir del programa
    def inicio_o_salir(self):
        opcion_elegida = input(f"""
Seleccione una opción:
[1] Volver al Menú de Inicio
[2] Salir del programa

Opción elegida: """)

        if (opcion_elegida.isdigit()):
            if int(opcion_elegida) == 1:
                self.elegir_opciones()

            elif int(opcion_elegida) == 2:
                self.salir_programa()
            
            else:
                print("Error. Solo puede ingresar números que se encuentren en las opciones.")
                self.inicio_o_salir()

        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.")
            self.inicio_o_salir()
        


    def salir_programa(self):
        print("Saliendo del programa...")
        return sys.exit()