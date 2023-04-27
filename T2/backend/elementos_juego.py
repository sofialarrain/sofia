from PyQt5.QtCore import QObject, QTimer, QRect
import backend.parametros as p
from backend.funciones import (seleccionar_ruta_guisante, seleccionar_ruta_planta, 
                                seleccionar_ruta_zombie)
 

class LanzaGuisante(QObject):

    def __init__(self, numero_casilla, tipo):
        super().__init__()
        self.tipo = tipo
        self.numero = numero_casilla
        self.esperando_disparar = False
        self.estado = 1
        self._vida = p.VIDA_PLANTA
        self.vivo = True

        # Configrar timer disparo (crear guisante)
        self.timer_disparo = QTimer()  # Crea guisantes
        self.timer_disparo.setInterval(p.INTERVALO_DISPARO)
        self.timer_disparo.timeout.connect(self.disparar)

        # Configurar timer estado (simular mov disparo)
        self.timer_cambiar_estado = QTimer()  # Simula movimiento diparo
        self.timer_cambiar_estado.setInterval(500)
        self.timer_cambiar_estado.timeout.connect(self.cambiar_estado)
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        if valor > 0:
            self._vida = valor
        else:
            self._vida = 0
            self.vivo = False
        
    def iniciar_timer(self):
        self.timer_disparo.start()

    def stop_timer(self):
        self.timer_disparo.stop()
    
    def disparar(self):
        self.esperando_disparar = True
    
    def cambiar_estado(self):
        if self.estado == 1:
            self.estado = 2
        elif self.estado == 2:
            self.estado = 3
        elif self.estado == 3:
            self.estado = 1
            self.timer_cambiar_estado.stop()

    def iniciar_cambio_estado(self):
        self.esperando_disparar = False
        self.timer_cambiar_estado.start()
    
    def stop_cambio_estado(self):
        self.timer_cambiar_estado.stop()
    
    def ruta(self):
        ruta = seleccionar_ruta_planta(self.tipo, self.estado)
        return ruta


class Girasol(QObject):

    def __init__(self, numero_casilla):
        super().__init__()
        self.tipo = "girasol"
        self.numero = numero_casilla
        self.esperando_generar_soles = False
        self.esperando_bailar = False
        self.estado = 1
        self._vida = p.VIDA_PLANTA
        self.vivo = True

        # Configrar timer generar soles
        self.timer_generar_soles = QTimer()
        self.timer_generar_soles.setInterval(p.INTERVALO_SOLES_GIRASOL)
        self.timer_generar_soles.timeout.connect(self.generar_soles)

        # Configurar timer bailar
        self.timer_bailar = QTimer()
        self.timer_bailar.setInterval(p.INTERVALO_BAILAR_GIRASOL)
        self.timer_bailar.timeout.connect(self.bailar)
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        if valor > 0:
            self._vida = valor
        else:
            self._vida = 0
            self.vivo = False
    
    def ruta(self):
        ruta = seleccionar_ruta_planta(self.tipo, self.estado)
        return ruta
    
    def iniciar_timer(self):
        self.timer_generar_soles.start()
        self.timer_bailar.start()
    
    def stop_timer(self):
        self.timer_generar_soles.stop()
        self.timer_bailar.stop()

    def generar_soles(self):
        self.esperando_generar_soles = True
    
    def bailar(self):
        if self.estado == 1:
            self.estado = 2
        else:
            self.estado = 1
        self.esperando_bailar = True


class Patata(QObject):

    def __init__(self, numero_casilla):
        super().__init__()
        self.tipo = "patata"
        self.numero = numero_casilla
        self.vida = p.VIDA_PLANTA * 2
        self.estado = 1
        self.vivo = True
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        if valor > 0:
            self._vida = valor
        else:
            self._vida = 0
            self.vivo = False
    
    def ruta(self):
        ruta = seleccionar_ruta_planta(self.tipo, self.estado)
        return ruta


class Zombie(QObject):

    numero = 1

    def __init__(self, fila_aparicion, tipo):
        super().__init__()
        self._x = p.X_POSICION_FINAL_CASILLAS
        self.fila = fila_aparicion
        self.ancho = p.ANCHO_ZOMBIE
        self.alto = p.ALTO_ZOMBIE
        self._vida = p.VIDA_ZOMBIE
        self.estado = 1
        self.ralentizado = False
        self.comiendo = False
        self.velocidad = p.VELOCIDAD_ZOMBIE
        self.comiendo_cerebros = False
        self.esperando_morder = False
        self.numero = Zombie.numero
        self.tipo = tipo
        self.vivo = True
        Zombie.numero += 1
        self.definir_Y()

        # Configurar timer mordida
        self.timer_mordida = QTimer()
        self.timer_mordida.setInterval(p.INTERVALO_TIEMPO_MORDIDA)
        self.timer_mordida.timeout.connect(self.mordida)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, valor):
        if valor <= p.X_POSICION_INICIAL_CASILLAS:
            self.comiendo_cerebros = True
            self._x = valor
        else:
            self._x = valor
    
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        if valor > 0:
            self._vida = valor
        else:
            self._vida = 0
            self.vivo = False

    def posicion(self):
        return QRect(self.x, self.y, p.ANCHO_ZOMBIE, p.ALTO_ZOMBIE)

    def definir_Y(self):
        if self.fila == 1:
            self.y = p.Y_FILA_1
        elif self.fila == 2:
            self.y = p.Y_FILA_2
    
    def mover(self):
        if not self.comiendo:
            if self.estado == 1:
                self.estado = 2
            else:
                self.estado = 1
            if self.tipo == "walker":
                self.x -= int(self.velocidad)
            elif self.tipo == "runner":
                self.x -= int(self.velocidad * 1.5)
        return (self.x, self.y)
    
    def ralentizar(self):
        ralentizar_v = self.velocidad * p.RALENTIZAR_ZOMBIE
        self.velocidad -= ralentizar_v
        self.ralentizado = True
    
    def iniciar_timer_mordida(self):
        self.comiendo = True   
        self.estado = 3
        self.timer_mordida.start()
    
    def stop_timer_mordida(self):
        self.comiendo = False
        self.estado = 1
        self.timer_mordida.stop()
    
    def mordida(self):
        if self.estado == 3:
            self.estado = 4
        elif self.estado == 4:
            self.estado = 5
        else:
            self.estado = 3
        self.esperando_morder = True
        
    def ruta(self):
        ruta = seleccionar_ruta_zombie(self.tipo, self.estado)
        return ruta
         
                
class Guisante(QObject):

    numero = 1

    def __init__(self, x, y, tipo):
        super().__init__()
        self.x = x
        self.y = y
        self.numero = Guisante.numero
        self.tipo = tipo
        self.vivo = True
        self.impactar = False
        self.estado = 1
        self.num_zombie_eliminar = ""
        Guisante.numero += 1

        # Configurar timer impactos
        self.timer_impacto = QTimer()
        self.timer_impacto.setInterval(600)
        self.timer_impacto.timeout.connect(self.impacto)
    
    def posicion(self):
        return QRect(self.x, self.y, p.ANCHO_GUISANTE, p.ALTO_GUISANTE)

    def mover(self):
        self.x += p.VELOCIDAD_GUISANTE
        return (self.x, self.y)
    
    def impacto(self):
        if self.estado == 1:
            self.estado = 2
        elif self.estado == 2:
            self.estado = 3
        elif self.estado == 3:
            self.estado = 4
        elif self.estado == 4:
            self.impactar = False
            self.vivo = False
            self.timer_impacto.stop()
    
    def iniciar_impacto(self):
        self.impactar = True
        self.timer_impacto.start()
    
    def ruta(self):
        ruta = seleccionar_ruta_guisante(self.tipo, self.estado)
        return ruta
    

class Sol(QObject):

    numero = 1

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.ancho = p.ANCHO_SOL
        self.alto = p.ALTO_SOL
        self.numero = Sol.numero
        self.tipo = "sol"
        self.vivo = True
        Sol.numero += 1


class Casilla(QObject):

    contador = 1
    x_inicio_casilla = p.X_POSICION_INICIAL_CASILLAS
    y_inicio_casilla = p.Y_POSICION_INICIAL_CASILLAS

    def __init__(self):
        super().__init__()
        self.ancho = p.ANCHO_CASILLA
        self.alto = p.ALTO_CASILLA
        self.numero = Casilla.contador
        self.libre = True
        self.x = [Casilla.x_inicio_casilla, Casilla.x_inicio_casilla + self.ancho]
        self.y = [Casilla.y_inicio_casilla, Casilla.y_inicio_casilla + self.alto]
        Casilla.x_inicio_casilla += self.ancho
        if Casilla.contador % 10 == 0:
            Casilla.x_inicio_casilla = p.X_POSICION_INICIAL_CASILLAS
            Casilla.y_inicio_casilla += self.alto
        Casilla.contador += 1
    
    def posicion(self):
        return QRect(self.x[0], self.y[0], self.ancho, self.alto)
    
    def plantar(self, planta):
        self.planta = planta
        self.libre = False
