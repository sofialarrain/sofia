# Tarea 2: DCCruz vs Zombies :zombie::seedling::sunflower:

**NOMBRE:** Sofía Larraín Vial

**CURSO:** Programación Avanzada (IIC2233)

**SECCIÓN:** 3

**USUARIO GITHUB:** sofialarrain

**FECHA:** 16/10/2022

## Consideraciones generales :octocat:

- El flujo funciona correctamente y no identifique ninngún error.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Simbología:
- ❌ no completado
- ✅ completado
- 🟠 incompleto
#### Ventanas: 39 pts (40%)
##### ✅ Ventana de Inicio
##### ✅ Ventana de Ranking	
##### ✅ Ventana principal
##### ✅ Ventana de juego	
##### ✅ Ventana post-ronda
#### Mecánicas de juego: 46 pts (47%)			
##### ✅ Plantas
##### ✅ Zombies
##### ✅ Escenarios		
##### ✅ Fin de ronda	
##### ✅ Fin de juego	
#### Interacción con el usuario: 22 pts (23%)
##### ✅ Clicks	
##### ✅ Animaciones
#### Cheatcodes: 8 pts (8%)
##### ✅ Pausa
##### ✅ S + U + N
##### ✅ K + I + L
#### Archivos: 4 pts (4%)
##### ✅ Sprites
##### ✅ Parametros.py
#### Bonus: 9 décimas máximo
##### ✅ Crazy Cruz Dinámico
##### ✅ Pala
##### ❌ Drag and Drop Tienda
##### ✅ Música juego

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. 
Además de este, la tarea contiene los siguientes módulos, archivos y directorios:
1. ```ventana_inicio.py``` en ```frontend``` 
2. ```ventana_ranking.py``` en ```frontend``` 
3. ```ventana_principal.py``` en ```frontend```  
4. ```ventana_ronda.py``` en ```frontend``` 
5. ```ventana_post_ronda.py``` en ```frontend``` 
6. ```elementos_juego.py``` en ```backend```
7. ```funciones.py``` en ```backend```
8. ```parametros.py``` en ```backend```
9. ```conecciones.py``` en ```backend```
10. ```logica_inicio.py``` en ```backend```
11. ```logica_ranking.py``` en ```backend```
12. ```logica_ronda.py``` en ```backend```
10. ```ventana_inicio.ui``` en ```ventanas```
11. ```ventana_principal.ui``` en ```ventanas```
12. ```ventana_ranking.ui``` en ```ventanas```
13. ```ventana_ronda.ui``` en ```ventanas```
14. ```ventana_post_ronda.ui``` en ```ventanas```
15. ```aparicion_zombies.py```
16. ```puntajes.txt```
17. ```sonidos```
18. ```sprites```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5.QtWidgets```: ```QApplication()```, ```QLabel()``` / ```conecciones.py```, ```ventana_ronda.py```
2. ```PyQt5.QtCore```: ```QObject()```, ```QTimer()```, ```QRect()```, ```pyqtSignal()```, ```Qt()``` / ```elementos_juego.py```, ```logica_inicio.py```, ```logica_ronda.py```, ```ventana_inicio.py```, ```ventana_post_ronda.py```, ```ventana_principal.py```, ```ventana_ronda.py```
3. ```random```: ```choice()```, ```randint()``` / ```funciones.py```
4. ```PyQt5.QtWidgets```: ```QApplication()``` / ```conecciones.py```
5. ```PyQt5.QtMultimedia```: ```QSound()``` / ```logica_inicio.py```, ```logica_ranking.py```, ```logica_ronda.py```, ```ventana_post_ronda.py```, ```ventana_principal.py```
6. ```os```: ```path()``` / ```parametros.py```
7. ```PyQt5```: ```uic``` / ```ventana_inicio.py```, ```ventana_principal.py```, ```ventana_ronda.py```
8. ```PyQt5.QtGui```: ```QPixmap()``` / ```ventana_ronda.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```ventana_inicio.py```: controla la parte visual de la ventana de inicio.
2. ```ventana_ranking.py```: controla la parte visual de la ventana de ranking.
3. ```ventana_principal.py```: muestra la ventana principal del juego que permite definir el escenario de la ronda.
4. ```ventana_ronda.py```: controla la parte visual de la ventana de la ronda actual.
5. ```ventana_post_ronda.py```: muestra la ventana post-ronda que da un resumen de ronda jugada anteriormente
6. ```elementos_juego.py```: contiene a las clases Lanzaguisante, Girasol, Patata, Zombie, Sol, Casilla
7. ```funciones.py```: contiene funciones que permiten simplificar el codigo del modulo **logica_ronda.py**
8. ```logica_inicio.py```: se encarga de validar usuarios y controlar la música.
9. ```logica_ranking.py```: se encarga de ordenar el ranking y actualizarlos.
11. ```logica_ronda.py```: se encarga de todo el funcionamiento detras de la ronda de jugada.
10. ```parametros.py```: contiene los parametros del juego.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

- La ventana principal y ventana post-ronda funcionan sin backend ya que no requieren de trabajo lógico, solo trabajo visual.
- No elimine objetos de listas cuando estos morian o desaparecian de la pantalla ya que las listas al ser revisadas a alta velocidad 
y en todo momento podian generar problemas. Estos se eliminan de las listas cuando las rondas terminan.
- Para hacer más efectivo la revision de listas se revisan solo los objetos que esten vivos.
- Las funciones de "sun" y "kill" solo funcionan mientras la ronda haya iniciado.
- Para matar a todos los zombies y aparecer soles se debe teclear "sun" o "kil" en un intervalo de tiempo de 1 segundo. (cada 1 seg las teclas registradas se resetean)
- Los movimientos de los guisantes se actualizar más rapido que los de los zombies y se controla con el contador velocidad.
- Las colisiones se detectan revisando la lista de zombies. Se recorre la lista y se va revisando si el zombie esta vivo o no. 
Luego se revisa si intersecta con un guisante y finalmente si sigue vivo se revisa si intersecta con una planta.
- Para eliminar los labels al terminar las rondas utilice .crear() ya que usando .deleteLater() o .destroy() se generaban errores.
- Los mensajes de crazy cruz se muestras durante 4 segundos y luego desaparecen.
- El mensaje final se muestra durante 5 segundos y luego se abre automaticamente la ventana de post-ronda y se esconde la ventana de ronda.

Sonidos:  
**crazyCruz_1.wav**: cuando casilla esta ocupada  
**crazyCruz_2.wav**: cuando no se tiene los soles necesarios para avanzar   
**crazyCruz_3.wav**: cuando no se tiene los soles necesarios para plantar  
**crazyCruz_4.wav**: cuando jugador gana una ronda   
**crazyCruz_5.wav**: cuando comienza una ronda  
**crazyCruz_6.wav**: cuando jugador pierde una ronda   
**musica.wav**: ventana de inicio   
**musica2.wav**: ventana principal, ventama ranking, ventana ronda, ventana post-ronda


-------
