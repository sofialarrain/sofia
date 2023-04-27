from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect
from backend.elementos_juego import (Guisante, Casilla, LanzaGuisante, Sol, Zombie, Girasol, Patata)
import backend.parametros as p
from aparicion_zombies import intervalo_aparicion
import backend.funciones as f
from PyQt5.QtMultimedia import QSound

class LogicaRonda(QObject):

    senal_actualizar_datos = pyqtSignal(dict)
    senal_preparar_escenario = pyqtSignal(str, int)
    senal_plantar = pyqtSignal(str, int)
    senal_crear_label = pyqtSignal(str, int, str, QRect)
    senal_actualizar_movimientos = pyqtSignal(dict)
    senal_eliminar_objeto = pyqtSignal(str, int)
    senal_deteriorar_patata = pyqtSignal(int, str)
    senal_terminar_ronda = pyqtSignal(dict)
    senal_mensaje = pyqtSignal(str)
    senal_mensaje_final = pyqtSignal(str)
    senal_habilitar_botones = pyqtSignal(bool)
    senal_actualizar_ranking = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()
        self.casillas = {}
        self.crear_casillas()
        self.musica = QSound(p.RUTA_MUSICA_2)  # Sonidos
        self.sonido_1 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_1)
        self.sonido_2 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_2)
        self.sonido_3 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_3)
        self.sonido_4 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_4)
        self.sonido_5 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_5)
        self.sonido_6 = QSound(p.RUTA_SONIDO_CRAZY_CRUZ_6)
    
    def configurar_timers(self):
        self.timer_actualizar_ronda = QTimer()  # Actualizar ronda
        self.timer_actualizar_ronda.setInterval(p.ACTUALIZAR_RONDA)
        self.timer_actualizar_ronda.timeout.connect(self.actualizar_ronda)
        self.timer_actualizar_eventos_teclas = QTimer()  # Teclas
        self.timer_actualizar_eventos_teclas.setInterval(p.ACTUALIZAR_EVENTOS_TECLAS)
        self.timer_actualizar_eventos_teclas.timeout.connect(self.actualizar_eventos_teclas)
        self.timer_aparecer_zombies = QTimer()  # Aparición zombies
        intervalo = intervalo_aparicion(self.nivel, self.ponderador)  
        self.timer_aparecer_zombies.setInterval(int(intervalo * 10000)) 
        self.timer_aparecer_zombies.timeout.connect(self.aparecer_zombies)
        self.timer_aparecer_soles = QTimer()  # Aparición soles
        self.timer_aparecer_soles.setInterval(p.INTERVALO_APARICION_SOLES)  
        self.timer_aparecer_soles.timeout.connect(self.generar_soles_escenario)
    
    def crear_casillas(self):
        for i in range(1, 21):
            self.casillas[i] = Casilla()

    def preparar_ronda(self, usuario, escenario, nivel, puntaje_total):
        self.usuario = usuario
        self.escenario = escenario
        self.nivel = nivel
        self.puntaje_total = puntaje_total
        if escenario == "diurno":
            self.ponderador = p.PONDERADOR_DIURNO
        elif escenario == "nocturno":
            self.ponderador = p.PONDERADOR_NOCTURNO
        self.configurar_timers()
        self.resetear_valores()
        self.senal_preparar_escenario.emit(escenario, nivel)
        self.musica.play()
    
    def resetear_valores(self):
        self.zombies = []
        self.guisantes = []
        self.plantas = []
        self.soles_jardin = []
        self.soles = 250
        self.puntaje = 0
        self.zombies_destruidos = 0
        self.zombies_restantes = p.N_ZOMBIES * 2
        self.zombies_fila_1 = 0
        self.zombies_fila_2 = 0
        self.ronda_pausada = True
        self.estado_ronda = ""
        self.ronda_comenzada = False
        self.planta_seleccionada = None
        self.eventos_teclas = ""
        self.contador_velocidad = 0
        self.actualizar_datos()

    def iniciar(self):
        self.senal_mensaje.emit(" A matar zombies! ")
        self.sonido_5.play()
        self.ronda_comenzada = True
        self.ronda_pausada = False
        self.timer_actualizar_ronda.start()
        self.timer_actualizar_eventos_teclas.start()
        self.timer_aparecer_zombies.start()
        if self.escenario == "diurno":
            self.timer_aparecer_soles.start()
        for planta in self.plantas:
            if planta.tipo != "patata":
                planta.iniciar_timer()
    
    def stop_musica(self):
        self.musica.stop()
    
    def pausar(self):
        if not self.ronda_pausada:
            self.ronda_pausada = True
            self.musica.stop()
            self.senal_habilitar_botones.emit(False)
            self.timer_actualizar_ronda.stop()
            self.timer_actualizar_eventos_teclas.stop()
            self.timer_aparecer_zombies.stop()
            if self.escenario == "diurno":
                self.timer_aparecer_soles.stop()
            for planta in self.plantas:
                if planta.tipo != "patata":
                    planta.stop_timer()
            for zombie in self.zombies:
                if zombie.comiendo:
                    zombie.stop_timer_mordida()
        else:
            self.ronda_pausada = False
            self.musica.play()
            self.senal_habilitar_botones.emit(True)
            self.timer_actualizar_ronda.start()
            self.timer_actualizar_eventos_teclas.start()
            self.timer_aparecer_zombies.start()
            if self.escenario == "diurno":
                self.timer_aparecer_soles.start()
            for planta in self.plantas:
                if planta.tipo != "patata":
                    planta.iniciar_timer()
            for zombie in self.zombies:
                if zombie.comiendo:
                    zombie.iniciar_timer_mordida()
    
    def avanzar(self):
        if self.soles >= p.COSTO_AVANZAR:
            self.estado_ronda = "ganada"
            self.soles -= p.COSTO_AVANZAR
            self.terminar_ronda()
        elif self.soles < p.COSTO_AVANZAR:
            self.senal_mensaje.emit(" No puedes avanzar. No tienes suficientes soles ")
            self.sonido_2.play()

    def generar_soles(self, numero_casilla):
        for _ in range(p.CANTIDAD_SOLES):
            geometry = f.geometry_sol("planta", self.casillas[numero_casilla])
            sol = Sol(geometry.x(), geometry.y())
            self.soles_jardin.append(sol)
            self.senal_crear_label.emit("sol", sol.numero, p.RUTA_SOL, geometry)

    def generar_soles_escenario(self):
        for _ in range(p.CANTIDAD_SOLES):
            geometry = f.geometry_sol("escenario", 0)
            sol = Sol(geometry.x(), geometry.y())
            self.soles_jardin.append(sol)
            self.senal_crear_label.emit("sol", sol.numero, p.RUTA_SOL, geometry)

    def aparecer_zombies(self):
        aparecer_zombies = True
        fila = f.elegir_fila_zombie(self.zombies_fila_1, self.zombies_fila_2)
        if fila == 1:
            self.zombies_fila_1 += 1
        elif fila == 2:
            self.zombies_fila_2 += 1
        elif fila == 0:
            aparecer_zombies = False
            self.timer_aparecer_zombies.stop()
        if aparecer_zombies:
            zombie = Zombie(fila, f.elegir_tipo_zombie())
            self.zombies.append(zombie)
            geometry = QRect(zombie.x, zombie.y, p.ANCHO_ZOMBIE, p.ALTO_ZOMBIE)
            self.senal_crear_label.emit("zombie", zombie.numero, zombie.ruta(), geometry)

    def seleccionar_girasol(self):
        self.planta_seleccionada = "girasol"

    def seleccionar_planta_clasica(self):
        self.planta_seleccionada = "clasica"

    def seleccionar_planta_azul(self):
        self.planta_seleccionada = "azul"

    def seleccionar_patata(self):
        self.planta_seleccionada = "patata"

    def seleccionar_pala(self):
        self.planta_seleccionada = "pala"
    
    def revisar_mouse_press_event(self, x, y, boton):
        if boton == "izquierdo":
            if (x in range(p.ANCHO_PASTO[0], p.ANCHO_PASTO[1]) and
                y in range(p.ALTO_PASTO[0], p.ALTO_PASTO[1])):
                for i in range(1, 21):
                    casilla = self.casillas[i]
                    if (x > casilla.x[0] and x < casilla.x[1] and
                        y > casilla.y[0] and y < casilla.y[1]):
                        if self.planta_seleccionada != "pala":
                            if casilla.libre:
                                if self.planta_seleccionada is not None:
                                    self.plantar(self.planta_seleccionada, casilla.numero)
                                    self.planta_seleccionada = None
                            else:
                                self.senal_mensaje.emit(" Casilla ocupada ")
                                self.sonido_1.play()
                        else:
                            casilla.libre = True
                            casilla.planta.vivo = False
                            self.senal_eliminar_objeto.emit("planta", casilla.numero)
            else:
                self.senal_mensaje.emit(" Solo puedes plantar en el terreno verde ")
        elif boton == "derecho":
            for sol in self.soles_jardin:
                if sol.vivo:
                    if (x > sol.x and x < sol.x + sol.ancho and y > sol.y and y < sol.y + sol.alto):
                        self.senal_eliminar_objeto.emit("sol", sol.numero)
                        self.soles += f.soles(self.escenario)
                        sol.vivo = False
      
    def revisar_tecla(self, tecla):
        if tecla == "p":
            self.pausar()
        elif tecla in "sunkil":
            self.eventos_teclas += tecla
            if self.eventos_teclas == "sun":
                self.soles += p.SOLES_EXTRA
            elif self.eventos_teclas == "kil":
                self.estado_ronda = "ganada"
                self.zombies_destruidos = p.N_ZOMBIES * 2
                self.zombies_restantes = 0
                self.actualizar_datos()
                self.terminar_ronda()
    
    def actualizar_eventos_teclas(self):
        self.eventos_teclas = ""  # Resetear teclas guardadas
    
    def plantar(self, tipo_planta, numero_casilla):
        casilla = self.casillas[numero_casilla]
        plantada = False
        if tipo_planta == "girasol" and self.soles >= p.COSTO_GIRASOL:
            planta = Girasol(numero_casilla)
            self.soles -= p.COSTO_GIRASOL
            plantada = True
        elif tipo_planta == "clasica" and self.soles >= p.COSTO_LANZAGUISANTE:
            planta = LanzaGuisante(numero_casilla, "clasica")
            self.soles -= p.COSTO_LANZAGUISANTE
            plantada = True
        elif tipo_planta == "azul" and self.soles >= p.COSTO_LANZAGUISANTE_HIELO:
            planta = LanzaGuisante(numero_casilla, "azul")
            self.soles -= p.COSTO_LANZAGUISANTE_HIELO
            plantada = True
        elif tipo_planta == "patata" and self.soles >= p.COSTO_PAPA:
            planta = Patata(numero_casilla)
            self.soles -= p.COSTO_PAPA
            plantada = True
        if plantada:
            self.plantas.append(planta)
            casilla.plantar(planta)
            self.senal_plantar.emit(planta.ruta(), numero_casilla)
            if self.ronda_comenzada and tipo_planta != "patata":
                planta.iniciar_timer()
            elif not self.ronda_comenzada:
                self.actualizar_datos()
        else:
            self.senal_mensaje.emit(" No tienes los soles necesarios ")
            self.sonido_3.play()
    
    def disparar(self, tipo_guisante, numero_casilla):
        casilla = self.casillas[numero_casilla]
        casilla.planta.iniciar_cambio_estado()
        geometry = f.geometry_gis(casilla)
        if tipo_guisante == "clasico":
            guisante = Guisante(geometry.x(), geometry.y(), "clasico")
        elif tipo_guisante == "azul":
            guisante = Guisante(geometry.x(), geometry.y(), "azul")
        self.guisantes.append(guisante)
        self.senal_crear_label.emit("guisante", guisante.numero, guisante.ruta(), geometry)

    def actualizar_datos(self):
        self.senal_actualizar_datos.emit({
            'Soles': self.soles, 'Zombies destruidos': self.zombies_destruidos,
            'Puntaje': self.puntaje, 'Zombies restantes': self.zombies_restantes})

    def actualizar_ronda(self):
        self.contador_velocidad += 1
        self.actualizar_datos()
        self.revisar_colisiones()
        for guisante in self.guisantes:  # Actualizar movimientos guisantes
            if guisante.vivo or guisante.impactar:
                if not guisante.impactar:  # Mover guisante
                    pos = guisante.mover()
                    self.senal_actualizar_movimientos.emit({"numero": guisante.numero, "x": pos[0], 
                        "y": pos[1], "tipo objeto": "guisante", "ruta": "", "accion": "mover"})
                else:
                    if guisante.estado == 2 or guisante.estado == 3:  # Impactar guisante
                        self.senal_actualizar_movimientos.emit({"numero": guisante.numero, 
                                "x": guisante.x, "y": guisante.y, "tipo objeto": "guisante",
                                "ruta": guisante.ruta(), "accion": "impactar"}) 
                    elif guisante.estado == 4:
                        self.senal_eliminar_objeto.emit("guisante", guisante.numero)
                        if guisante.num_zombie_eliminar != "":
                            self.senal_eliminar_objeto.emit("zombie", guisante.num_zombie_eliminar)
        if self.contador_velocidad % 4 == 0:  # Actualizar movimientos zombies 
            for zombie in self.zombies:
                if zombie.vivo:
                    pos = zombie.mover()  # Solo cambia posición si no esta comiendo
                    self.senal_actualizar_movimientos.emit({"numero": zombie.numero, 
                        "x": pos[0], "y": pos[1], "tipo objeto": "zombie", "ruta": zombie.ruta()}) 
                    if zombie.comiendo_cerebros:
                        self.estado_ronda = "perdida"
                        self.terminar_ronda()
        for planta in self.plantas:  # Revisar generar soles y disparos de plantas
            if planta.vivo:
                if planta.tipo == "girasol":
                    if planta.esperando_generar_soles:
                        planta.esperando_generar_soles = False
                        self.generar_soles(planta.numero)
                    if planta.esperando_bailar:
                        planta.esperando_bailar = False
                        self.senal_actualizar_movimientos.emit({"numero": planta.numero, "x": "", 
                            "y": "", "tipo objeto": "planta", "ruta": planta.ruta()})
                elif planta.tipo == "clasica" or planta.tipo == "azul":
                    if planta.esperando_disparar:
                        planta.iniciar_cambio_estado()                
                    if planta.estado == 3:
                        geometry = f.geometry_gis(self.casillas[planta.numero])
                        if planta.tipo == "clasica":
                            guisante = Guisante(geometry.x(), geometry.y(), "clasico")
                        elif planta.tipo == "azul":
                            guisante = Guisante(geometry.x(), geometry.y(), "azul")
                        self.guisantes.append(guisante) 
                        self.senal_crear_label.emit(
                            "guisante", guisante.numero, guisante.ruta(), geometry)
                    self.senal_actualizar_movimientos.emit({"numero": planta.numero, "x": "", 
                            "y":"", "tipo objeto": "planta", "ruta": planta.ruta()})
        if self.zombies_restantes == 0:
            self.estado_ronda = "ganada"
            self.actualizar_datos()
            self.terminar_ronda()
    
    def revisar_colisiones(self):
        for zombie in self.zombies:
            if zombie.vivo:
                for guisante in self.guisantes:  # Colision zombie-guisante
                    if guisante.vivo and not guisante.impactar:
                        if guisante.posicion().intersects(zombie.posicion()):
                            if not guisante.impactar:  # Interseccion puede durar segundos
                                zombie.vida -= p.DANO_PROYECTIL
                                guisante.iniciar_impacto()
                                if guisante.tipo == "azul":
                                    if not zombie.ralentizado:
                                        zombie.ralentizar()
                            if zombie.vida == 0:
                                self.zombies_destruidos += 1
                                self.zombies_restantes -= 1
                                self.puntaje += f.puntaje(self.escenario)
                                guisante.num_zombie_eliminar = zombie.numero
                if zombie.vivo:  # Colision zombie-planta 
                    debe_comer = False
                    for i in range(1, 21):
                        casilla = self.casillas[i]
                        if not casilla.libre and casilla.posicion().intersects(zombie.posicion()):
                            debe_comer = True
                            planta = casilla.planta
                            if not zombie.comiendo:
                                zombie.iniciar_timer_mordida()
                            else:
                                if zombie.esperando_morder:
                                    zombie.esperando_morder = False
                                    planta.vida -= p.DANO_MORDIDA
                                    if planta.vida > 0:
                                        if planta.tipo == "patata":
                                            ruta = f.ruta_deteriorar(planta)
                                            self.senal_deteriorar_patata.emit(planta.numero, ruta)
                                    else:
                                        zombie.stop_timer_mordida()
                                        casilla.libre = True
                                        self.senal_eliminar_objeto.emit("planta", planta.numero)
                    if not debe_comer and zombie.comiendo:
                        zombie.stop_timer_mordida()                          

    def terminar_ronda(self):
        self.pausar()
        self.puntaje_ronda = f.calcular_ptotal(self.puntaje, self.ponderador, self.estado_ronda)
        for i in range(1, 21):
            self.casillas[i].libre = True
        if self.estado_ronda == "ganada":
            self.sonido_4.play()
            self.senal_mensaje_final.emit("mensaje ganar")
        elif self.estado_ronda == "perdida":
            self.sonido_6.play()
            self.senal_mensaje_final.emit("mensaje perder")

    def enviar_datos(self):
        self.senal_actualizar_ranking.emit(self.usuario, self.puntaje_total + self.puntaje_ronda)
        self.senal_terminar_ronda.emit({'Usuario': self.usuario, 'Ronda actual': self.nivel,
            'Soles restantes': self.soles, 'Zombies destruidos': self.zombies_destruidos,
            'Puntaje ronda': self.puntaje_ronda, 'Estado ronda': self.estado_ronda,
            'Puntaje total': self.puntaje_total + self.puntaje_ronda})
        self.musica.stop()
