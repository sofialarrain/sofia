from os import path


# Intervalos (en milisegundos)
INTERVALO_DISPARO = 3000
INTERVALO_SOLES_GIRASOL = 10000
INTERVALO_APARICION_SOLES = 10000
INTERVALO_TIEMPO_MORDIDA = 1000
INTERVALO_BAILAR_GIRASOL = 1500

# Daños
DANO_PROYECTIL = 5
DANO_MORDIDA = 5

# Número de zombies por carril
N_ZOMBIES = 7

# Porcentaje de ralentización
RALENTIZAR_ZOMBIE = 0.25

# Soles iniciales por ronda
SOLES_INICIALES = 250

# Número de soles generados por planta
CANTIDAD_SOLES = 2

# Número de soles agregados a la cuenta por recolección
SOLES_POR_RECOLECCION = 50

# Número de soles agregados a la cuenta por Cheatcode
SOLES_EXTRA = 25

# Ponderadores de escenarios
PONDERADOR_NOCTURNO = 0.8
PONDERADOR_DIURNO = 0.9

# Puntaje por eliminar zombie
PUNTAJE_ZOMBIE_DIURNO = 50
PUNTAJE_ZOMBIE_NOCTURNO = 100

# Costo por avanzar de ronda
COSTO_AVANZAR = 500

# Costo tiendas
COSTO_LANZAGUISANTE = 50
COSTO_LANZAGUISANTE_HIELO = 100
COSTO_GIRASOL = 50
COSTO_PAPA = 75

# Carácteres de nombre usuario
MIN_CARACTERES = 3
MAX_CARACTERES = 15

# Características Plantas 
VIDA_PLANTA = 10
ANCHO_PLANTA = 58
ALTO_PLANTA = 78

# Características Zombies
VIDA_ZOMBIE = 12
ANCHO_ZOMBIE = 58   
ALTO_ZOMBIE = 78
TIPO_ZOMBIE = ["runner", "walker"]
VELOCIDAD_ZOMBIE = 24 # divisible en 1.5

# Características Soles
ANCHO_SOL = 30
ALTO_SOL = 30

#  Características Guisantes
ANCHO_GUISANTE = 20
ALTO_GUISANTE = 20
VELOCIDAD_GUISANTE = 30

# Casillas
X_POSICION_INICIAL_CASILLAS = 256
Y_POSICION_INICIAL_CASILLAS = 166
X_POSICION_FINAL_CASILLAS = 874
ANCHO_CASILLA = 58                               
ALTO_CASILLA = 78

# Posiciones
X_APARICION_ZOMBIE = 874                    

# Filas
Y_FILA_1 = 166                              
Y_FILA_2 = 245

# Dimensiones escenario
ANCHO_JARDIN = [254, 875]                  
ALTO_JARDIN = [65, 430]
ANCHO_PASTO = 256, 875
ALTO_PASTO = 166, 323

# Juego
ACTUALIZAR_RONDA = 300
ACTUALIZAR_MOVIMIENTOS_ZOMBIES = 1000
ACTUALIZAR_MOVIMIENTOS_GUISANTES = 500
ACTUALIZAR_EVENTOS_TECLAS = 1000

# Rutas plantas
RUTA_GIRASOL_1 = path.join("sprites", "Plantas", "girasol_1.png")
RUTA_GIRASOL_2 = path.join("sprites", "Plantas", "girasol_2.png")
RUTA_PLANTA_CLASICA_1 = path.join("sprites", "Plantas", "lanzaguisantes_1.png")
RUTA_PLANTA_CLASICA_2 = path.join("sprites", "Plantas", "lanzaguisantes_2.png")
RUTA_PLANTA_CLASICA_3 = path.join("sprites", "Plantas", "lanzaguisantes_3.png")
RUTA_PLANTA_AZUL_1 = path.join("sprites", "Plantas", "lanzaguisantesHielo_1.png")
RUTA_PLANTA_AZUL_2 = path.join("sprites", "Plantas", "lanzaguisantesHielo_2.png")
RUTA_PLANTA_AZUL_3 = path.join("sprites", "Plantas", "lanzaguisantesHielo_3.png")
RUTA_PATATA_1 = path.join("sprites", "Plantas", "papa_1.png")
RUTA_PATATA_2 = path.join("sprites", "Plantas", "papa_2.png")
RUTA_PATATA_3 = path.join("sprites", "Plantas", "papa_3.png")

# Rutas Zombie
RUTA_RUNNER_CAMINANDO_1 = path.join("sprites", "Zombies", "Caminando", "zombieHernanRunner_1.png")
RUTA_RUNNER_CAMINANDO_2 = path.join("sprites", "Zombies", "Caminando", "zombieHernanRunner_2.png")
RUTA_WALKER_CAMINANDO_1 = path.join("sprites", "Zombies", "Caminando", "zombieNicoWalker_1.png")
RUTA_WALKER_CAMINANDO_2 = path.join("sprites", "Zombies", "Caminando", "zombieNicoWalker_2.png")
RUTA_RUNNER_COMIENDO_1 = path.join("sprites", "Zombies", "Comiendo", "zombieHernanComiendo_1.png")
RUTA_RUNNER_COMIENDO_2 = path.join("sprites", "Zombies", "Comiendo", "zombieHernanComiendo_2.png")
RUTA_RUNNER_COMIENDO_3 = path.join("sprites", "Zombies", "Comiendo", "zombieHernanComiendo_3.png")
RUTA_WALKER_COMIENDO_1 = path.join("sprites", "Zombies", "Comiendo", "zombieNicoComiendo_1.png")
RUTA_WALKER_COMIENDO_2 = path.join("sprites", "Zombies", "Comiendo", "zombieNicoComiendo_2.png")
RUTA_WALKER_COMIENDO_3 = path.join("sprites", "Zombies", "Comiendo", "zombieNicoComiendo_3.png")

# Guisantes
RUTA_GUISANTE_CLASICO_1 = path.join("sprites", "Elementos de juego", "guisante_1.png")
RUTA_GUISANTE_CLASICO_2 = path.join("sprites", "Elementos de juego", "guisante_2.png")
RUTA_GUISANTE_CLASICO_3 = path.join("sprites", "Elementos de juego", "guisante_3.png")
RUTA_GUISANTE_AZUL_1 = path.join("sprites", "Elementos de juego", "guisanteHielo_1.png")
RUTA_GUISANTE_AZUL_2 = path.join("sprites", "Elementos de juego", "guisanteHielo_2.png")
RUTA_GUISANTE_AZUL_3 = path.join("sprites", "Elementos de juego", "guisanteHielo_3.png")

# Rutas Elementos de juego
RUTA_LOGO = path.join("sprites", "Elementos de juego", "logo.png")
RUTA_SOL = path.join("sprites", "Elementos de juego", "sol.png")
RUTA_TEXTO_FINAL = path.join("sprites", "Elementos de juego", "textoFinal.png")
RUTA_CRAZY_RUZ = path.join("sprites", "Elementos de juego", "crazyCruz.png")

# Rutas Ventanas
RUTA_VENTANA_INICIO = path.join("ventanas", "ventana_inicio.ui")
RUTA_VENTANA_RANKING = path.join("ventanas", "ventana_ranking.ui")
RUTA_VENTANA_PRINCIPAL = path.join("ventanas", "ventana_principal.ui")
RUTA_VENTANA_JUEGO = path.join("ventanas", "ventana_ronda.ui")
RUTA_VENTANA_POST_RONDA = path.join("ventanas", "ventana_post_ronda.ui")

# Bonus
RUTA_PALA = path.join("sprites", "Bonus", "pala.png")

# Sonidos
RUTA_SONIDO_CRAZY_CRUZ_1 = path.join("sonidos", "crazyCruz_1.wav")  # Hablando
RUTA_SONIDO_CRAZY_CRUZ_2 = path.join("sonidos", "crazyCruz_2.wav")  # Retando
RUTA_SONIDO_CRAZY_CRUZ_3 = path.join("sonidos", "crazyCruz_3.wav")  # Retando
RUTA_SONIDO_CRAZY_CRUZ_4 = path.join("sonidos", "crazyCruz_4.wav")  # Felicitando
RUTA_SONIDO_CRAZY_CRUZ_5 = path.join("sonidos", "crazyCruz_5.wav")  # Comentando
RUTA_SONIDO_CRAZY_CRUZ_6 = path.join("sonidos", "crazyCruz_6.wav")  # $%!?$&#
RUTA_MUSICA_1 = path.join("sonidos", "musica.wav")
RUTA_MUSICA_2 = path.join("sonidos", "musica2.wav")
