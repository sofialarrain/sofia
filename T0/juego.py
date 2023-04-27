from parametros import POND_PUNT 
import tablero
import os
import os.path
import inicio

class MenuJuego:

    def __init__(self):
        self.nombre_archivo = ""
        self.nombre_usuario = ""
        self.ancho_tablero = 0
        self.largo_tablero = 0
        self.cantidad_bestias = 0
        self.tablero = []
        self.tablero2 = []
        self.casillas_descubiertas = 0
        self.puntajes = 0


    def comenzar_juego(self, archivo_partida):

        self.nombre_archivo = archivo_partida

        #guardar información de la partida creada para comenzar juego
        path = os.path.join("partidas", self.nombre_archivo)

        with open(path, "rt", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            self.nombre_usuario = lineas[0].strip()
            self.ancho_tablero = int(lineas[1])
            self.largo_tablero = int(lineas[2])
            self.cantidad_bestias = int(lineas[3])
            self.tablero = MenuJuego.convertir_tablero(lineas[4])
            self.tablero2 = MenuJuego.convertir_tablero(lineas[5])
            self.casillas_descubiertas = int(lineas[6])

        MenuJuego.elegir_opciones(self)


    def elegir_opciones(self):

        print(f"""
MENU DE JUEGO

Estado actual del tablero:
""")
        tablero.print_tablero(self.tablero2, True)

        print(f"""
Seleccione una de las siguientes opciones:
[1] Descubir un sector
[2] Guardar la partida
[3] Salir de la partida
""")  
        opcion_elegida = input("Opción elegida: ")

        if (opcion_elegida.isdigit()):
            if int(opcion_elegida) == 1:
                MenuJuego.descubrir_sector(self)

            elif int(opcion_elegida) == 2:
                MenuJuego.guardar_partida(self)

            elif int(opcion_elegida) == 3:
                MenuJuego.salir_partida(self)

            else:
                print("Error. Solo puede ingresar números que se encuentren en las opciones.")
                MenuJuego.elegir_opciones(self)
        
        else:
            print("Error. Solo puede ingresar números que se encuentren en las opciones.")
            MenuJuego.elegir_opciones(self)  
        

    def descubrir_sector(self):

        print("Has decidido descubir un sector del tablero.")

        letra_ancho_tablero = chr(self.ancho_tablero + 96).upper()

        #aclarar requicitos de las coordenadas
        print(f"""
Eliga una columna de la A a la {letra_ancho_tablero}.
Luego, una fila del 0 al {self.largo_tablero - 1}.
""")

        #ingresar coordenada x
        coordenada_x_correcta = False
        while not coordenada_x_correcta:
            coordenada_x = input(f"Ingrese columna: ")

            if (coordenada_x.isdigit()):
                print("Error. Debe ingresar una letra.")
            
            else:
                if len(coordenada_x) > 1:
                    print("Error. Debe ingresar una letra.")
                
                else:
                    x = ord(coordenada_x.lower()) - 97
                    coordenada_x = x

                    if coordenada_x < 0 or coordenada_x > self.ancho_tablero - 1:
                        print("Error. Debe ingresar una letra dentro de las dimensiones del tablero.")
                    
                    else: 
                        coordenada_x_correcta = True


        #ingresar coordenada y
        coordenada_y_correcta = False
        while not coordenada_y_correcta:
            coordenada_y = input("Ingrese fila: ") 

            if (coordenada_y.isdigit()):
                if int(coordenada_y) < 0 or int(coordenada_y) > self.largo_tablero - 1:
                    print("Error. Debe ingresar un número dentro de las dimensiones del tablero.")

                else:
                    y = int(coordenada_y)
                    coordenada_y = y 
                    coordenada_y_correcta = True

            else:
                print("Error. Debe ingresar un número dentro de las dimensiones del tablero.")
            

        #revisar si coordenada escogida ya fue descubierta, esta vacia, o hay una bestia (muere)

        #casilla vacia
        if self.tablero[coordenada_y][coordenada_x] == " ":
            print("\nBien! Esta casilla se encuentra libre de bestias Nexus.")
            self.casillas_descubiertas += 1

            MenuJuego.contar_bestias_cerca(self, coordenada_y , coordenada_x)
            
            #revisar si gana la partida
            cantidad_casillas_sin_bestias = (self.ancho_tablero * self.largo_tablero) - self.cantidad_bestias
            if self.casillas_descubiertas == cantidad_casillas_sin_bestias:
                print("Felicitaciones! Has descubierto todo el plan del malvado Canciller y has ganado la partida.")
                MenuJuego.termino_partida(self)
            
            else:
                print("Puedes seguir buscando bestias Nexus.")
                MenuJuego.elegir_opciones(self)

        #casilla con bestia
        elif self.tablero[coordenada_y][coordenada_x] == "N":
            print("\nTe has encontrado con una bestia Nexus!. Has perdido.")
            MenuJuego.termino_partida(self)
            
        #casilla ya descubierta
        else:
            print("\nEsta casilla ya ha sido descubierta!")
            MenuJuego.elegir_opciones(self)


    def guardar_partida(self):

        print("Guardando partida...")
        
        #escribir informacion en archivo
        path = os.path.join("partidas", self.nombre_archivo)

        with open(path, "wt", encoding="utf-8") as archivo:
            archivo.write(self.nombre_usuario + "\n" + str(self.ancho_tablero) + "\n" \
                + str(self.largo_tablero) + "\n" + str(self.cantidad_bestias) + "\n" \
                    + str(self.tablero) + "\n" + str(self.tablero2) + "\n" \
                        + str(self.casillas_descubiertas))
                           
        MenuJuego.elegir_opciones(self)
        
    
    #convierte string de tablero en lista de listas
    def convertir_tablero(string):

        tablero = []
        filas = string.strip("[[").strip("]]\n").split("], [")

        for fila in filas:
            f = fila.split(", ")
            fila_nueva = []

            for posicion in f:
                p = posicion.strip("'")
                fila_nueva.append(p)
                
            tablero.append(fila_nueva)
        
        return tablero

    
    #recibe coordenada y cuenta las bestias que la rodean
    def contar_bestias_cerca(self, coordenada_y, coordenada_x):
        cantidad_bestias_cerca = 0

        #revisar 3 casillas de arriba   
        if coordenada_y - 1 >= 0:
            if coordenada_x - 1 >= 0:
                if self.tablero[coordenada_y - 1][coordenada_x - 1] == "N":
                    cantidad_bestias_cerca += 1

            if self.tablero[coordenada_y - 1][coordenada_x] == "N":
                cantidad_bestias_cerca += 1
            
            if coordenada_x + 1 <= self.ancho_tablero - 1:
                if self.tablero[coordenada_y - 1][coordenada_x + 1] == "N":
                    cantidad_bestias_cerca += 1

        #revisar 3 casillas abajo
        if coordenada_y + 1 <= self.largo_tablero - 1:
            if coordenada_x - 1 >= 0:
                if self.tablero[coordenada_y + 1][coordenada_x - 1] == "N":
                    cantidad_bestias_cerca += 1
            
            if self.tablero[coordenada_y + 1][coordenada_x] == "N":
                cantidad_bestias_cerca += 1

            if coordenada_x + 1 <= self.ancho_tablero - 1:
                if self.tablero[coordenada_y + 1][coordenada_x + 1] == "N":
                    cantidad_bestias_cerca += 1

        #revisar casilla izquierda
        if coordenada_x - 1 >= 0:
            if self.tablero[coordenada_y][coordenada_x - 1] == "N":
                cantidad_bestias_cerca += 1

        #revisar casilla derecha
        if coordenada_x + 1 <= self.ancho_tablero - 1:
            if self.tablero[coordenada_y][coordenada_x + 1] == "N":
                cantidad_bestias_cerca += 1

        self.tablero[coordenada_y][coordenada_x] = str(cantidad_bestias_cerca)
        self.tablero2[coordenada_y][coordenada_x] = str(cantidad_bestias_cerca)

        if cantidad_bestias_cerca == 0:
            MenuJuego.expandir(self, coordenada_y, coordenada_x)
    

    #recibe coordenada a la cual no la rodean bestias y descubre todas las casillas adyacentes
    def expandir(self, coordenada_y, coordenada_x):

        #revisar 3 casillas de arriba   
        if coordenada_y - 1 >= 0:
            if coordenada_x - 1 >= 0:
                if self.tablero[coordenada_y - 1][coordenada_x - 1] == " ":
                    MenuJuego.contar_bestias_cerca(self, coordenada_y - 1, coordenada_x - 1)
                    self.casillas_descubiertas += 1
                    
            if self.tablero[coordenada_y - 1][coordenada_x] == " ":
                MenuJuego.contar_bestias_cerca(self, coordenada_y - 1, coordenada_x)
                self.casillas_descubiertas += 1
            
            if coordenada_x + 1 <= self.ancho_tablero - 1:
                if self.tablero[coordenada_y - 1][coordenada_x + 1] == " ":
                    MenuJuego.contar_bestias_cerca(self, coordenada_y - 1, coordenada_x + 1)
                    self.casillas_descubiertas += 1
        
        #revisar 3 casillas abajo
        if coordenada_y + 1 <= self.largo_tablero - 1:
            if coordenada_x - 1 >= 0:
                if self.tablero[coordenada_y + 1][coordenada_x - 1] == " ":
                    MenuJuego.contar_bestias_cerca(self, coordenada_y + 1, coordenada_x - 1)
                    self.casillas_descubiertas += 1
            
            if self.tablero[coordenada_y + 1][coordenada_x] == " ":
                MenuJuego.contar_bestias_cerca(self, coordenada_y + 1, coordenada_x)
                self.casillas_descubiertas += 1

            if coordenada_x + 1 <= self.ancho_tablero - 1:
                if self.tablero[coordenada_y + 1][coordenada_x + 1] == " ":
                    MenuJuego.contar_bestias_cerca(self, coordenada_y + 1, coordenada_x + 1)
                    self.casillas_descubiertas += 1

        #revisar casilla izquierda
        if coordenada_x - 1 >= 0:
            if self.tablero[coordenada_y][coordenada_x - 1] == " ":
                MenuJuego.contar_bestias_cerca(self, coordenada_y, coordenada_x - 1)
                self.casillas_descubiertas += 1

        #revisar casilla derecha
        if coordenada_x + 1 <= self.ancho_tablero - 1:
            if self.tablero[coordenada_y][coordenada_x + 1] == " ":
                MenuJuego.contar_bestias_cerca(self, coordenada_y, coordenada_x + 1)
                self.casillas_descubiertas += 1


    def salir_partida(self):
        print("Has salido de la partida...")    

        #si el jugador no guardó partida, sólo quedara la información creada en el inicio
        #lo realizado en la partida se perderá

        inicio.MenuInicio.elegir_opciones(self)

    
    def termino_partida(self):  

        self.puntajes = self.cantidad_bestias * self.casillas_descubiertas * POND_PUNT

        print(f"""
Fin de la partida.

Tablero final:
""")

        tablero.print_tablero(self.tablero, False)

        print(f"""
Nombre Usuario: {self.nombre_usuario}
Puntaje Final: {self.puntajes}
""")

        #si hay puntajes registrados:
        if os.path.exists("puntajes.txt"):

            #revisar si usuario ya tiene un puntaje registrado
            puntaje_registrado = False
            with open("puntajes.txt", "rt", encoding="utf-8") as archivo:
                lineas = archivo.readlines()

            #en caso de que el puntaje este registrado:
            #se vuelve a escribir archivo linea por linea
            #si puntaje es mayor al registrado, se escribira otra linea con el puntaje actualizado
            with open("puntajes.txt", "wt", encoding="utf-8") as archivo:
                for linea in lineas:
                    usuario = linea[:linea.find(":")]
                    puntaje = int(linea[linea.find(":") + 1:].strip("\n"))

                    #busca nombre del jugador en los puntajes registrados 
                    if self.nombre_usuario == usuario:
                        puntaje_registrado = True

                        #revisa si el puntaje registrado es menor al obtenido actualmente
                        if self.puntajes > puntaje:
                            archivo.write(self.nombre_usuario + ":" + str(self.puntajes) + "\n")
                        else:
                            archivo.write(linea)
                    else: 
                        archivo.write(linea)
            
            #en caso de que el puntaje no este registrado:
            if not puntaje_registrado:                 
                with open("puntajes.txt", "a", encoding="utf-8") as archivo:
                    archivo.write(self.nombre_usuario + ":" + str(self.puntajes) + "\n")


        #si no hay puntajes registrados:
        else:
            with open("puntajes.txt", "wt", encoding="utf-8") as archivo:
                archivo.write(self.nombre_usuario + ":" + str(self.puntajes) + "\n")


        #eliminar archivo de partida porque ya se cerró la partida
        path = os.path.join("partidas", self.nombre_archivo)
        os.remove(path)

        inicio.MenuInicio.elegir_opciones(self) 