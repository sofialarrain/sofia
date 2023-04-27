# Tarea 3: DCCard-Jitsu 🐧🥋


**NOMBRE:** Sofía Larraín Vial

**CURSO:** Programación Avanzada (IIC2233)

**SECCIÓN:** 3

**USUARIO GITHUB:** sofialarrain

**FECHA:** 15/11/2022

## Consideraciones generales :octocat:
El flujo funciona correctamente y no identifique ningún error. :)


### Cosas implementadas y no implementadas :white_check_mark: :x:

Simbología:
- ❌ no completado
- ✅ completado
- 🟠 incompleto
#### Networking: 26 pts (19%)
##### ✅ Protocolo	
##### ✅ Correcto uso de sockets		
##### ✅ Conexión	
##### ✅ Manejo de Clientes	
##### ✅ Desconexión Repentina
#### Arquitectura Cliente - Servidor: 31 pts (23%)			
##### ✅ Roles			
##### ✅ Consistencia		
##### ✅ Logs
#### Manejo de Bytes: 27 pts (20%)
##### ✅ Codificación			
##### ✅ Decodificación			
##### ✅ Encriptación		
##### ✅ Desencriptación	
##### ✅ Integración
#### Interfaz Gráfica: 27 pts (20%)	
##### ✅ Ventana inicio		
##### ✅ Sala de Espera			
##### ✅ Ventana de juego							
##### ✅ Ventana final
#### Reglas de DCCard-Jitsu: 17 pts (13%)
##### ✅ Inicio del juego			
##### ✅ Ronda				
##### ✅ Termino del juego
#### Archivos: 8 pts (6%)
##### ✅ Parámetros (JSON)		
##### ✅ Cartas.py	
##### ✅ Cripto.py
#### Bonus: 8 décimas máximo
##### ✅ Cheatcodes	
##### ✅ Bienestar	
##### ❌ Chat

## Ejecución :computer:
Para la ejecución del programa primero se debe ejecutar el módulo ```main.py``` del servidor desde el entorno de la carpta ```servidor```. Luego para conectar a los clientes se debe ejecutar el módulo ```main.py``` del cliente desde el entorno de la carpeta ```cliente```. Todo lo anterior desde la terminal.

Además de este, la tarea contiene los siguientes módulos, archivos y directorios:
1. ```archivo_cliente.py``` en ```cliente\backend```
2. ```cripto.py``` en ```cliente\backend```
3. ```interfaz.py``` en ```cliente\backend```
3. ```sprites``` en ```cliente\frontend```
4. ```ventana_inicio.ui``` en ```cliente\frontend\ventanas_uic```
5. ```ventana_espera.ui``` en ```cliente\frontend\ventanas_uic```
6. ```ventana_juego.ui``` en ```cliente\frontend\ventanas_uic```
7. ```ventana_final.ui``` en ```cliente\frontend\ventanas_uic```
8. ```ventana_inicio.py``` en ```cliente\frontend```
9. ```ventana_espera.py``` en ```cliente\frontend```
10. ```ventana_juego.py``` en ```cliente\frontend```
11. ```ventana_final.py``` en ```cliente\frontend```
11. ```funciones.py``` en ```cliente```
12. ```parametros.json``` en ```cliente```
13. ```cartas.py``` en ```scripts\servidor```
14. ```archivo_servidor.py``` en ```servidor```
15. ```cripto.py``` en ```servidor```
16. ```funciones.py``` en ```servidor```
17. ```logica_servidor.py``` en ```servidor```
18. ```parametros.json``` en ```servidor```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5.QtWidgets```: ```QApplication()```, ```QLabel()``` / ```ventana_juego.py```, ```main.py```
2. ```PyQt5.QtCore```: ```QObject()```, ```pyqtSignal()```, ```QTimer``` / ```archivo_cliente.py```, ```interfaz.py```, ```ventana_inicio.py```, ```ventana_espera.py```, ```ventana_juego.py```, ```ventana_final.py```, ```funciones.py```
3. ```random```: ```choice()``` / ```funciones.py```
4. ```socket``` / ```archivo_cliente.py```, ```main.py```, ```archivo_servidor.py```
5. ```os.path()```: ```join()``` / ```ventana_inicio.py```, ```ventana_espera.py```, ```ventana_juego.py```, ```ventana_final.py```, ```funciones.py```
6. ```PyQt5```: ```uic``` / ```ventana_inicio.py```, ```ventana_espera.py```, ```ventana_juego.py```, ```ventana_final.py```
7. ```PyQt5.QtGui```: ```QPixmap()```,  ```QIcon()```/ ```ventana_juego.py```
8. ```json``` / ```archivo_cliente.py```, ```funciones.py```, ```archivo_servidor.py```
9. ```threading```: ```Thread``` / ```archivo_cliente.py```, ```archivo_servidor.py```
10. ```math``` / ```cripto.py```
11. ```time```: ```sleep``` / ```ventana_juego.py```, ```funciones.py```
12. ```sys``` / ```main.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```archivo_cliente.py```: contiene la clase **Cliente**. Esta clase cuenta con funciones que le permiten conectarse al servidor y comunicarse con el a traves de mensajes encriptados y luego codificados.
2. ```archivo_servidor.py```: contiene la clase **Servidor**. Esta clase cuenta con funciones que le permiten conectarse con diferentes clientes a la vez y poder comunicarse con ellos simultaneamente.
3. ```logica_servidor.py```: contiene la clase **LogicaServidor** que se encarga de procesar los mensajes recibidos por los clientes y generar respuestas que permiten el flujo del juego. 
4. ```interfaz.py```: interpreta los mensajes recibidos del cliente de parte del servidor, genera respuestas y envia señales a las respectivas ventanas.
5. ```ventana_inicio.py```: controla la parte visual de la ventana de inicio.
6. ```ventana_espera.py```: controla la parte visual de la ventana de espera.
7. ```ventana_juego.py```: controla la parte visual de la ventana de juego.
8. ```ventana_final.py```: controla la parte visual de la ventana de final.
9. ```cripto.py```: contiene las funciones para encriptar y desenciptar mensajes. Hay dos de estos módulos iguales, uno en la carpeta de cliente y otro en la del servidor.
10. ```funciones.py```: contiene funciones que permiten simplificar el código de los demás módulos y facilitan su ejecución. Hay dos de estos módulos, uno en la carpeta de cliente y otro en la del servidor. El perteneciente a la carpeta servidor contiene además las clases **SalaEspera**, **Juego**, **Jugador** y **CuentaRegresiva**.
11. ```parametros.json```: contiene parametros en un archivo formato .json. Hay dos de estos archivos, uno en la carpeta de cliente y otro en la del servidor.
12. ```main.py```: El perteneciente a la carpeta cliente, inicia el cliente y conecta las señales entre la interfaz y las ventanas. El perteneciente a la carpeta servidor, inicia el servidor.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Cuando un jugador se desconecta automaticamente se desconecta de la sala de espera y libera un cupo.
2. Los usuarios solo se registran una vez que ingresan a la sala de espera. Cuando un jugador termina una partida y vuelve a la ventana de inicio su nombre de usuario se elimina. Solo estarán registrados los usuarios que se encuentren dentro de una partida.
3. Agregue más logs de los pedidos de manera que se me hiciera más sencilla la construcción del código.
4. Cuando dos cartas tienen mismo elemento y valor empatan sin importar su color.
5. Además de la cuenta regresiva de la ronda le sume una cuenta regresiva de pocos segundos para mostrar las cartas jugadas, el jugador ganador de la ronda y el jugador perdedor de la ronda o si fue empate. En estos segundos las cartas de la bandeja estan bloquiadas.
6. Cuando un jugador intenta entrar a la sala de espera pero está llena se notifica en la interfaz del jugador que sala no tiene capacidad, en cambio si intenta y hay dos jugadores en una partida se notifica que hay un juego en curso.
7. Cuando un jugador junta las fichas necesarias y gana la partida, se abre automáticamente la ventana final.
8. Antes de chequear si un jugador puede entrar a la sala de espera, verifica si el usuario es válido, por lo que solo mostrara el mensaje de sala llena si se ingreso un usuario válido.

Bonus:
1. Cuando un jugador usa el boton de bienestar, gana una carta al azar de su maso. En cambio el oponente no presenta ninguna carta ya que este perdera de todas formas.
2. Si un jugador intenta usar el boton de bienestar y no tiene fichas de 3 colores distintos se muestra un mensaje en la interfaz. Si cumple la condicion anterior, el boton se usa y se inhabilita por el resto de la partida para ese jugador. 
3. El cheatcode "veo" solo muestra la carta del oponente si esque este tiene alguna seleccionada. En caso contrario no pasa nada.



## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. El código relacionado con la arquitectura cliente-servidor lo hice basandome en lo realizado en la actividad formativa 3, los contenidos vistos en clases y la ayudantía.