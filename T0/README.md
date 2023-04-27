# Tarea 0: Star Advanced :school_satchel:
**NOMBRE:** Sofía Larraín Vial

**CURSO:** Programación Avanzada (IIC2233)

**SECCIÓN:** 3

**USUARIO GITHUB:** sofialarrain

**FECHA:** 29/08/2022


## Consideraciones generales :octocat:
- El código funciona correctamente y no tiene errores de ejecución.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Simbología:
- ❌  **NO** está completo lo pedido
- ✅ está **correctamente** completo lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

#### **Programación Orientada a Objetos (18pts) (22%%)**
##### ✅ Menú de Inicio: Hecha completa  
##### ✅ Funcionalidades: Hecha completa  
##### ✅ Puntajes: Hecha completa  
#### **Flujo del Juego (30pts) (36%)**
##### ✅ Menú de Juego: Hecha completa  
##### ✅ Tablero: Hecha completa  
##### ✅ Bestias: Hecha completa  
##### ✅ Guardado de partida: Hecha completa  
#### **Término del Juego 14pts (17%)** 
##### ✅ Fin del juego: Hecha completa  
##### ✅ Puntajes: Hecha completa  
#### **Genera: 15 pts (15%)**  
##### ✅ Menús: Hecha completa  
##### ✅ Parámetros: Hecha completa  
##### ✅ PEP-8: Hecha completa  
#### **Bonus: 3 décimas**  
##### ✅ : Hecha completa


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```flujo.py```. En este módulo solo se imprime la bienvenida al juego y se llama a una función del módulo ```inicio.py``` que comienza el fujo del programa.
Además de este, la tarea contiene los siguientes módulos, archivos y directorios:
1. ```inicio.py``` en ```T0``` 
2. ```juego.py``` en ```T0``` 
3. ```parametros.py``` en ```T0``` archivo entregado que contiene parametros.
4. ```tablero.py``` en ```T0``` archivo entregado que contiene funciones para imprimir tablero.
5. ```partidas``` en ```T0``` carpeta que contiene los archivos de las jugadas que **no han sido terminadas**.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. ```os``` : ```remove() / juego.py```
2. ```os.path``` : ```join(), isfile() / inicio.py, juego.py```
3. ```random``` : ```randint() / inicio.py```
4. ```math``` : ```ceil() / inicio.py```
5. ```sys``` : ```exit() / inicio.py```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. ```inicio```: Contiene a la clase ```MenuInicio``` que tiene funciones que se encargan de crear una partida nueva, cargar una existente, ver el ranking del juego o salir del programa.
2. ```juego```: Contiene a la clase ```MenuJuego``` que tiene funciones que se encargan de descubir un sector, guardar la partida o salir de la partida.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
- El código se compone de dos clases una llamada ```MenuInicio``` que se encarga de la preparación previa del juego y de la clase ```MenuJuego``` que se encarga de ejecutar las partidas y de controlar el tablero. 
- Dentro de las clases hay distintas funciones que actuan de manera recursiva lo que permiten un flujo eficiente.
- En el ```MenuInicio``` y en el ```MenuJuego``` existe una función que permite al jugador elegir opciones. Estas opciones llaman a las demás funciones y así permiten el desarrollo de la partida.
- El código tiene respuesta para cada input entregado al programa, sea número dentro de las opciones, número fuera de las opciones o caracteres alfabéticos.
- Cuando se crea una partida, se crea un archivo con la información de ésta y se guarda automaticamente en la carpeta ```partidas```, pero la información solo se ira actualizando a medida que el jugador seleccione guardar. Si un jugador decide salir de la partida y nunca guardó su partida, solo quedara registrada la información guardada cuando se creó la partida y su tablero sin ningún sector descubierto.
- Cuando un jugador pierde o gana, el archivo de su partida se elimina de la carpeta ```partidas```.
- Para que se pueda abrir la carpeta ```partidas``` de cualquier consola, se implementó un path relativo.

***Formato archivos (dentro de la carpeta partidas)***  
1. Nombre usuario
2. Ancho tablero  
3. Largo tablero
4. Cantidad bestias
5. Tablero (string de lista de listas, contiene bestias, tablero que se vera al terminar partida)
6. Tablero 2 (string de lista de listas, no contiene bestias, tablero que se vera en la partida)
6. Cantidad casillas descubiertas

***Formato puntajes.txt***  
nombre_usuario_1:puntaje  
nombre_usuario_2:puntaje    
***...***

-----
## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. [chr()](https://parzibyte.me/blog/2018/12/10/ord-chr-python/#:~:text=el%20c%C3%B3digo%20unicode-,La%20funci%C3%B3n%20ord%20en%20Python,el%2097%20y%20as%C3%AD%20sucesivamente.&text=Devuelve%20un%20entero%20que%20representa%20a%20ese%20car%C3%A1cter.): convierte números en letras y está implementado en el archivo ```juego.py``` en la línea ***<81>***. Recibe el ancho del tablero + 96 y este valor lo convierte en la letra que esta asignada a ese número. Los números estan relacionados con el orden del abecedario. (si la letra esta en mínuscula o mayúscula dan diferentes valores)

2. [ord()](https://parzibyte.me/blog/2018/12/10/ord-chr-python/#:~:text=el%20c%C3%B3digo%20unicode-,La%20funci%C3%B3n%20ord%20en%20Python,el%2097%20y%20as%C3%AD%20sucesivamente.&text=Devuelve%20un%20entero%20que%20representa%20a%20ese%20car%C3%A1cter.): convierte letras en números y está implementado en el archivo ```juego.py``` en la línea ***<102>***. Este sigue la misma lógica anterior pero de manera inversa.

3. [os.remove()](https://micro.recursospython.com/recursos/como-eliminar-un-archivo-o-carpeta.html#:~:text=Para%20eliminar%20un%20archivo%20se,remove()%20.&text=Para%20remover%20una%20carpeta%20vac%C3%ADa,rmdir()%20.): recibe un archivo y lo elimina y está implementado en el archivo ```juego.py``` en la línea ***<358>***.

4. [key=lambda](https://www.delftstack.com/es/howto/python/sort-list-of-lists-in-python/): junto con la función sort() ordena listas de listas y está implementado en el archivo ```inicio.py``` en la línea ***<205>***.

5. [os.path.exists()](https://geekflare.com/es/check-if-file-folder-exists-in-python/): revisa si existe una carpeta o archivo y esta implementado en el archivo ```inicio.py``` en las lineas ***<67>*** y ***<192>*** y en el archivo ```juego.py``` en la linea ***<317>***.

6. [os.mkdir()](https://j2logo.com/como-crear-directorios-en-python/): crea una carpeta y esta implementado en el archivo ```inicio.py``` en la linea ***<76>***.