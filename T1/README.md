# Tarea 1: DCCampeonato 🏃‍♂️🏆
**NOMBRE:** Sofía Larraín Vial

**CURSO:** Programación Avanzada (IIC2233)

**SECCIÓN:** 3

**USUARIO GITHUB:** sofialarrain

**FECHA:** 15/09/2022


## Consideraciones generales :octocat:
- El flujo funciona correctamente y no identifique ninngún error.


### Cosas implementadas y no implementadas :white_check_mark: :x:

Simbología:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Programación Orientada a Objetos (18pts) (22%%)
##### ✅ Diagrama
##### ✅ Definición de clases, atributos, métodos y properties		
##### ✅ Relaciones entre clases
#### Preparación programa: 11 pts (7%)			
##### ✅ Creación de partidas
#### Entidades: 28 pts (19%)
##### ✅ Programón
##### ✅ Entrenador		
##### ✅ Liga	
##### ✅ Objetos		
#### Interacción Usuario-Programa 57 pts (38%)
##### ✅ General	
##### ✅ Menú de Inicio
##### ✅ Menú Entrenador
##### ✅ Menu Entrenamiento
##### ✅ Simulación ronda campeonato
##### ✅ Ver estado del campeonato
##### ✅ Menú crear objeto
##### ✅ Menú utilizar objeto
##### ✅ Ver estado del entrenador
##### ✅ Robustez
#### Manejo de archivos: 12 pts (8%)
##### ✅ Archivos CSV
##### ✅ Parámetros
#### Bonus: 5 décimas
##### ✅ Mega Evolución
##### ✅ CSV dinámico

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. 
Además de este, la tarea contiene los siguientes módulos, archivos y directorios:
1. ```liga_programon.py``` en ```T1``` 
2. ```entrenadores.py``` en ```T1``` 
3. ```programones.py``` en ```T1``` 
4. ```objetos.py``` en ```T1``` 
5. ```menus.py``` en ```T1``` 
6. ```parametros.py``` en ```T1```
7. ```entrenadores.csv```, ```programones.csv```, ```objetos.csv``` y ```evoluciones.csv``` en ```T1``` (archivos entregados para crear el campeonato).


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. ```random``` : ```random()```, ```choice()```, ```randint()``` / ```entrenadores.py```, ```liga_programon.py```, ```objetos.py```, ```programones.py```
2. ```abc``` : ```ABC```, ```abstractmethod``` / ```objetos.py```, ```programones.py```
3. ```sys``` : ```exit()``` / ```menus.py```



### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. ```main.py```: en este módulo se leen los archivos ```entrenadores.csv```, ```programones.csv```, ```objetos.csv``` y ```evoluciones.csv```, los que permiten crear los respectivos objetos y agregarlos a sus respectivas listas. Luego con estas se crea el campeonato instanciando a **LigaProgramon** y comienza el campeonato llamando a la función menu_inicio() que inicia el flujo del prgrama.
2. ```liga_programon.py```: contiene a la clase **LigaProgramon**.
3. ```entrenadores.py```: contiene a la clase **Entrenador**.
4. ```programones.py```: contiene a la clase abstracta **Programon** y a las clases **TipoPlanta**, **TipoFuego** y **TipoAgua** que heredan de ésta. Estas representan programones de tipo planta, fuego y agua.
5. ```objetos.py```: contiene a la clase abstracta **Objeto** y a las clases **Baya** y **Pocion** que heredan de ésta. Además contiene a la clase **Caramelo** que recibe una multiherencia de las clases **Baya** y **Pocion**.
6. ```parametros.py```: contiene parametros constantes que permiten funcionar al programa.
7. ```menus.py```: contiene las funciones que permiten el flujo del programa e imprimen los menus del campeonato.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
- Cuando el entrenador escogido pierde una batalla, el programa lo notifica y se termina el campeonato aunque sigan quedando rondas. Luego, da al jugador las opciones de volver al menu de inicio para comenzar otro campeonato con otro entrenador o salir.
- El código tiene respuesta para cada input entregado al programa, sea número dentro de las opciones, número fuera de las opciones o caracteres alfabéticos.
- En el caso **poco probable** que dos rivales tengan el mismo puntaje de victoria se definira el rival 1 como ganador (lo que se podría interpretar como al azar ya que el rival 1 esta definido al azar).
- El entrenador escogido por el jugador siempre aparecerá en el primer enfrentamiento de las rondas.
- Cuando se utiliza un objeto, este se elimina.
- Cuando se intenta crear un objeto que ya existe, este se crea de igual manera mientas el entrenador tenga energía para hacerlo.

## **Diagrama de Clases**

### Las principales clases involucradas en DCCampeonato son:
1. LigaProgramon
2. Entrenador
3. Programon (abstracta)
4. Objeto (abstracta)
5. TipoPlanta
6. TipoFuego
7. TipoAgua
8. Baya
9. Pocion
10. Caramelo

### Las relaciones que existen entre ellas son de:  
**Composición:**  
- ```LigaPogramon``` incluye a ```Entrenador```. ```LigaProgramon``` puede tener más de 1 ```Entrenador```.  

**Agregación:**
- ```Programon``` asociado a ```Entrenador```. ```Entrenador``` puede tener más de un ```Programon```.  
- ```Objeto``` asociado a ```Entrenador```. ```Entrenador``` puede tener más de un ```Objeto```.  

**Herencia:**
- ```Planta```, ```Fuego``` y ```Agua``` son clases que heredan de la clase ```Programon```.
- ```Baya``` y ```Pocion``` son clases que heredan de la clase ```Objeto```.
- ```Caramelo``` es una clase que hereda de la clase ```Baya``` y ```Pocion```.

-----
