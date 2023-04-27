from PyQt5.QtCore import QObject, pyqtSignal


class LogicaRanking(QObject):

    senal_actualizar = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.puntajes = []
        self.crear_lista()
        self.ordenar_ranking()

    def crear_lista(self):
        with open("puntajes.txt", "rt", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                linea = linea.strip("\n").split(",")
                usuario = linea[0]
                puntaje = int(linea[1])
                self.puntajes.append([usuario, puntaje])
    
    def ordenar_ranking(self):
        self.puntajes.sort(key=lambda x: x[1], reverse=True)
    
    def actualizar_ventana(self):
        self.senal_actualizar.emit(self.puntajes)

    def actualizar_ranking(self, nuevo_usuario, nuevo_puntaje):
        # Revisar si usuario ya esta registrado
        puntaje_registrado = False
        with open("puntajes.txt", "rt", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        with open("puntajes.txt", "wt", encoding="utf-8") as archivo:
            for linea in lineas:
                usuario = linea[:linea.find(",")]
                puntaje = int(linea[linea.find(",") + 1:].strip("\n"))
                if usuario == nuevo_usuario:
                    puntaje_registrado = True
                    if nuevo_puntaje > puntaje:
                        archivo.write(nuevo_usuario + "," + str(nuevo_puntaje) + "\n")
                    else:
                        archivo.write(linea)
                    # Actualizar lista ranking
                    for puntaje in self.puntajes:
                        if puntaje[0] == nuevo_usuario:
                            puntaje[1] = nuevo_puntaje
                else:
                    archivo.write(linea)
        
        if not puntaje_registrado:              
            with open("puntajes.txt", "a", encoding="utf-8") as archivo:
                archivo.write(nuevo_usuario + "," + str(nuevo_puntaje) + "\n")
        
        # Volver a crear lista
        self.puntajes.clear()
        self.crear_lista()
        
        # Actualizar orden ranking
        self.ordenar_ranking()
    
        # Actualizar ventana
        self.senal_actualizar.emit(self.puntajes)
