# MEMORIA

## 1. Introducción

### 1.1 Resumen del Proyecto

El proyecto que se presenta en esta memoria consiste en el diseño, la arquitectura y el desarrollo de **Artemis 67**, un videojuego de plataformas en dos dimensiones (2D), con elementos de *Run and Gun* y programado en el lenguaje Python utilizando la librería gráfica Arcade (versión 3.3.3).

El jugador representa al piloto de la misión espacial Artemis 67, cuya nave es derribada sobre la superficie marciana y debe abrirse camino a través de cinco niveles ambientados en distintos entornos del planeta rojo para lograr escapar y regresar a la Tierra.

El juego combina mecánicas clásicas, como salto, gravedad y plataformas móviles, con un sistema de combate. A lo largo de los niveles el jugador se enfrenta a dos tipos de enemigos: zombies astronautas y aliens cerebrales.

El proyecto cuenta con una interfaz de menú completa. La música y los efectos de sonido se gestionan de forma persistente entre vistas, manteniendo el volumen configurado por el usuario en todo momento.


### 1.2 Objetivos

El objetivo principal de este proyecto ha sido desarrollar un videojuego de plataformas 2D completo y jugable, aplicando los conocimientos de programación orientada a objetos, gestión de recursos y diseño de videojuegos adquiridos durante la asignatura, utilizando Python y la biblioteca Arcade. Para ello, se plantearon los siguientes objetivos específicos:

- Implementar un sistema de combate con dos tipos de arma: un proyectil rápido de daño directo y un proyectil explosivo de área con mecánica de rocket jump.
- Diseñar dos tipos de enemigos con comportamientos diferenciados: patrulla y persecución para el zombie astronauta, y detección de rango con disparo dirigido para el alien cerebral.
- Construir cinco niveles mediante Tiled Map Editor con capas diferenciadas para plataformas, paredes destructibles, elementos de daño, plataformas móviles y escaleras.
- Desarrollar una interfaz de usuario completa con menú principal, selección de nivel, ajustes de audio y pantalla, guía de controles y pantalla de Game Over.
- Gestionar el audio de forma persistente entre vistas, con música diferenciada para el menú y el juego, y control de volumen global.
- Estructurar el código en módulos independientes aplicando programación orientada a objetos para facilitar el mantenimiento y la escalabilidad del proyecto.


## 2. Diseño del juego

### 2.1 Descripción de los niveles

- Nivel 1 — Polo Sur de Marte: Primer nivel del juego, ambientado en las regiones heladas del polo sur marciano. Sirve como introducción a las mecánicas básicas de movimiento y combate.
- Nivel 2 — Glaciar de Marte: Entorno de hielo y roca con plataformas de mayor dificultad. El jugador debe enfrentarse a los enemigos en un terreno más exigente.
- Nivel 3 — Superficie de Marte: Ambientado en la árida superficie marciana bajo un cielo rojizo. Nivel de dificultad intermedia con mayor presencia de enemigos.
- Nivel 4 — Caverna de Marte: Nivel subterráneo en el interior de una caverna marciana. La disposición cerrada de las plataformas aumenta la dificultad del combate.
- Nivel 5 — Volcanes de Marte: Nivel final ambientado en una zona volcánica activa. Es el nivel más exigente del juego, con mayor densidad de enemigos y elementos de daño en el entorno.

Los niveles se diseñan mediante Tiled Map Editor y se exportan en formato .tmj.

### 2.2 Diseño de personajes y enemigos

PROTAGONISTA — ASTRONAUTA
El jugador controla a un astronauta con animaciones direccionales completas: caminar, saltar y apuntar en múltiples direcciones. El personaje puede moverse horizontalmente, saltar y disparar en la dirección en la que mira. Sus animaciones se cargan desde spritesheets y se procesan en tiempo de ejecución.

ZOMBIE ASTRONAUTA
Enemigo de combate cuerpo a cuerpo. En modo patrulla se desplaza de un extremo al otro de la plataforma en la que se encuentra. Cuando el jugador entra dentro de su rango de visión, cambia al modo persecución y se lanza hacia él.

BRAIN ALIEN
Enemigo a distancia. Patrulla su plataforma hasta que detecta al jugador dentro de su rango de visión, momento en el que se detiene y dispara proyectiles dirigidos hacia él a una cadencia definida. Tiene mayor rango de detección que el zombie. 

### 2.3 Mecánicas del juego

MOVIMIENTO Y FÍSICAS
El personaje se desplaza horizontalmente y puede saltar. La gravedad se aplica de forma constante tanto al jugador como a los enemigos. El juego incluye plataformas móviles con las que el motor gestiona las colisiones automáticamente.

SALTO EXPLOSIVO
Es posible alcanzar un mayor rango de salto con el uso del disparo secundario, dicho salto es calculado en base al angulo de impacto respecto del jugador. Esta mecánica resulta util en algunos casos, en los que solamente se puede acceder de esta forma.

SISTEMA DE COMBATE
El jugador dispone de dos tipos de disparo:
- Disparo principal: Proyectil rápido de daño directo que inflige 25 puntos de daño. Tiene animación de impacto al colisionar con enemigos o superficies.
- Disparo secundario (explosivo): Proyectil más lento que al impactar genera una explosión en área con un radio de 150 píxeles, infligiendo 50 puntos de daño a todos los enemigos dentro del radio. Si el jugador abunta hacia abajo y dispara, recibe un impulso de empuje vertical (rocket jump) que le permite alcanzar zonas elevadas.

PAREDES DESTRUCTIBLES
Ciertos bloques del escenario tienen puntos de vida y pueden ser destruidos por los disparos del jugador, abriendo nuevos caminos en el nivel.

SISTEMA DE PUNTUACIÓN
El jugador acumula puntos al eliminar enemigos (150 puntos por enemigo) y al destruir bloques destructibles (50 puntos por bloque).

RECOGIDA DE PIEZAS
Es indispensable la recogida de una sola pieza por mapa para completar este, de lo contrario el personaje no podrá atravesar el portal y por tanto completar el mapa.

### 2.4 Diseño de la interfaz y menús

La interfaz está compuesta por las siguientes pantallas:

- Menú principal: Pantalla de inicio con acceso a jugar, reiniciar el progreso, ajustes, controles y salir. Reproduce música de fondo en bucle.
- Ajustes: Incluye un slider de control de volumen de la música y un toggle para activar o desactivar el modo pantalla completa. Los cambios se aplican en tiempo real y se mantienen al volver al menú.
- Controles: Pantalla informativa con la guía de controles del juego.
- Game Over: Se muestra al morir el jugador, con opciones para volver a intentar el nivel o regresar al menú principal.

Todas las pantallas se adaptan al tamaño de la ventana y son compatibles con el modo pantalla completa.

## 3. Arte y Assets

### 3.1 Sprites y Animaciones

Todos los sprites del juego han sido creados por el equipo de desarrollo. Cada personaje cuenta con múltiples animaciones direccionales organizadas en spritesheets de frames de 64×64 píxeles, que el juego procesa en tiempo de ejecución mediante PIL para recortar cada frame y generar automáticamente la versión correcta.
El astronauta protagonista dispone de animaciones de caminar y saltar en cinco direcciones: frontal, arriba, abajo, diagonal arriba y diagonal abajo. El zombie astronauta cuenta con animaciones de caminar en tres direcciones. El alien cerebral dispone de animaciones de caminar y de patrulla.

### 3.2 Diseño de Niveles y Tilesets

Los cinco niveles del juego han sido diseñados íntegramente por el equipo utilizando Tiled Map Editor. Cada nivel está construido mediante capas diferenciadas: plataformas estáticas, paredes, paredes destructibles, elementos de daño, plataformas móviles, escaleras y puntos de aparición de enemigos. 

### 3.3 Música y Efectos de Sonido

La música del juego ha sido elegida por el equipo de desarrollo. Se utilizan dos pistas diferenciadas: una para los menús ("Mythical Axiom") y otras 3 para los niveles ("Phase Shift", "Overflowing Core" y "Virus"), todas reproducidas en bucle. Los efectos de sonido (salto, disparo, impacto y game over) se gestionan mediante los recursos integrados de la librería Arcade.

### 3.4 Tipografía

Los textos de la interfaz utilizan la fuente Upheaval TT (BRK), cargada como recurso externo desde la carpeta de assets del proyecto, lo que garantiza que se muestre correctamente en cualquier sistema independientemente de las fuentes instaladas

## 4. Arquitectura técnica y programación

### 4.1 Tecnologías Utilizadas

El proyecto está desarrollado íntegramente en **Python**, utilizando la librería gráfica **Arcade 3.3.3** como motor del juego. Arcade proporciona el sistema de ventanas, el bucle de juego, la gestión de sprites, las físicas de plataformas, la reproducción de audio y la carga de mapas en formato Tiled.

Para el diseño de niveles se utiliza **Tiled Map Editor**, exportando los mapas en formato `.tmj` que Arcade carga dinámicamente. El procesamiento de spritesheets para las animaciones de los personajes se realiza con **PIL (Pillow)**, recortando y volteando cada frame manualmente para generar las versiones normal y espejada de cada animación. La gestión de rutas de archivos se lleva a cabo con la librería estándar `pathlib`, lo que permite que el proyecto funcione correctamente independientemente del sistema operativo o del directorio desde el que se ejecute. La persistencia de datos se gestiona con la librería estándar `json`.

### 4.2 Estructura del código

El código está dividido en módulos independientes, cada uno con una responsabilidad clara:

- **`constants.py`:** Contiene todas las constantes del proyecto (dimensiones de la ventana, velocidades, rutas de assets, parámetros de enemigos y proyectiles, y la estructura de datos iniciales del sistema de guardado).
- **`main.py`:** Contiene la clase `GameView`, que es el núcleo del juego. Gestiona el bucle principal, la carga del mapa, la creación de personajes y enemigos, las físicas, los controles, el sistema de disparo, la cámara, la puntuación y el sistema de activación espacial de enemigos. También contiene la clase `PauseView` para la pantalla de pausa y la función `main()` que inicializa la ventana.
- **`character.py`:** Define la jerarquía de personajes mediante clases: `PlayerCharacter` para el jugador, `ZombieEnemy` y `AlienEnemy` para los enemigos. Cada clase gestiona sus propias animaciones, comportamiento y lógica de actualización. Las texturas se procesan con PIL mediante la función `load_spritesheet_pair`, que genera automáticamente la versión normal y la espejada de cada animación.
- **`projectile.py`:** Implementa la jerarquía de proyectiles. La clase base `ProyectilBase` define la lógica común de movimiento y colisión. De ella heredan `DisparoPrincipal`, `DisparoSecundario` (con explosión en área y rocket jump) y `AlienProyectile`, cada uno con comportamiento propio.
- **`serializacion.py`:** Gestiona la lectura y escritura del archivo de guardado `savegame.json` mediante las funciones `cargar_datos()` y `guardar_datos()`. Si el archivo no existe o está corrupto, lo regenera automáticamente con los valores iniciales.
- **`mainMenu.py`:** Gestiona la pantalla del menú principal, incluyendo la carga y reproducción de la música del menú y el botón de nueva partida que resetea el progreso guardado.
- **`ajustes.py`:** Pantalla de ajustes con control de volumen mediante slider y toggle de pantalla completa. Los cambios se aplican en tiempo real y persisten entre vistas.
- **`controles.py`:** Pantalla informativa con la guía de controles del juego.
- **`gameOver.py`:** Pantalla de Game Over con opciones para reintentar el nivel o volver al menú.

### 4.3 Gestión de Vistas

Todas las pantallas del juego heredan de `arcade.View`, lo que permite cambiar entre ellas sin cerrar ni reiniciar la ventana. La ventana (`arcade.Window`) actúa como contenedor persistente que mantiene el estado compartido entre vistas: el nivel seleccionado, el volumen de la música y las referencias al reproductor de audio y a la vista de juego activa.

### 4.4 Cámaras y Resolución

El juego utiliza dos cámaras simultáneas para separar el mundo del juego de la interfaz:

- **`self.camera`:** Cámara del mundo de juego. Sigue al jugador horizontalmente con límites en los bordes del mapa: no se desplaza si el jugador está en el primer o último tramo del nivel, evitando que se vea fuera del mapa.
- **`self.gui_camera`:** Cámara fija para la interfaz. Se usa para dibujar la puntuación, el indicador de carga del disparo secundario y los elementos de la pausa siempre en la misma posición de pantalla, independientemente de dónde esté la cámara del mundo.

### 5. Detalles técnicos

### 5.1 Algoritmo de activación de enemigos

Para evitar la saturación del procesador al gestionar mapas con multiples entidades simultáneas, se ha implementado un algoritmo de optimización de rendimiento basado en la proximidad. El bucle de actualización del juego recorre la lista completa de enemigos en cada fotograma y calcula la distancia exacta respecto del jugador, si la distancia resultante es superior a la distancia en píxeles establecida, el motor suspende automáticamente la ejecución de la "máquina de estados" de la IA del enemigo y detiene la comprobación de sus colisiones con el entorno. Las entidades permanecen congeladas en memoria hasta que el jugador entra en su radio de activación, reduciendo el consumo de CPU.

### 5.2 Sistema de gestión de colisiones 
El motor físico de Artemis 67 procesa las colisiones de manera segmentada para optimizar el rendimiento y permitir interacciones diferenciadas con el entorno. Al cargar el mapa en formato .tmj, el código no genera una única malla de colisión, sino que separa los elementos en SpriteList independientes según las capas de diseño:

Capa de Paredes y Plataformas: Alimenta el motor de físicas principal, permitiendo tanto al personaje como a los enemigos caminar sobre plataformas, bajar y subirlas, en definitiva , seguir un movimiento real evitando traspasos de paredes o que cualquier elemento pueda salirse del mapa por ejemplo.

Capa de Elementos de Daño: Ejecuta un bucle secundario que comprueba colisiones mediante la intersección de cajas alineadas. Si se detecta solapamiento con el jugador, salta inmediatamente al GameOver por muerte.

Capa de Bloques Destructibles: Al impactar un proyectil de la lista DisparoPrincipal o DisparoSecundario, el algoritmo calcula el identificador del tile colisionado, resta puntos de durabilidad a dicho bloque y, al llegar a cero, elimina el sprite de la capa y actualiza el sistema de puntuación sumando 50 puntos de forma reactiva.

## Conclusiones

El desarrollo de este videojuego ha supuesto un reto enorme, pero al mismo tiempo ha sido una de las experiencias más enriquecedoras de nuestra formación. Partir desde un concepto inicial hasta lograr un producto interactivo, jugable y funcional ha requerido una gran dedicación y un esfuerzo por parte de todo el equipo.

Este proyecto nos ha permitido consolidar nuestros conocimientos en la programación orientada a objetos utilizando Python y la librería Arcade. A lo largo de las semanas, hemos aprendido a enfrentarnos a problemas reales y complejos del desarrollo de videojuegos. Hemos interiorizado conceptos avanzados como la gestión de estados (transiciones entre menús principales, niveles, pantallas de pausa y Game Over), la adaptación dinámica de cámaras y resoluciones, el manejo eficiente de recursos (spritesheets, sistemas de audio persistentes) y la optimización del rendimiento en pantalla. Enfrentarnos a bugs difíciles y aprender a leer los errores nos ha dado una visión mucho más profunda y profesional sobre la arquitectura del software.

Por otro lado, trabajar en grupo nos ha enseñado lecciones que van mucho más allá de escribir código. Hemos aprendido a coordinarnos, a integrar diferentes módulos programados por distintas personas y a comunicarnos de forma efectiva para resolver los conflictos que surgían al juntar las piezas. Entender el código de un compañero, buscar soluciones conjuntas y apoyarnos en los momentos de frustración ha sido vital para sacar el proyecto adelante.

En definitiva, el balance final del proyecto es sumamente positivo. Aunque el camino ha estado lleno de desafíos y quebraderos de cabeza, la satisfacción de ver nuestro juego funcionando, hace que todo el esfuerzo haya merecido la pena. Nos llevamos un aprendizaje técnico y personal inmenso, y una base de conocimientos para afrontar cualquier proyecto de desarrollo en el futuro.

## Anexo I
MUSICA
"Mythical Axiom" - Part of “Honkai: Star Rail - Allegory of the Cave (Part 3)” Original Game Soundtrack · Author: HOYO-MIX ℗ 2025 HOYO-MiX [Mythical Axiom Youtube link](https://www.youtube.com/watch?v=qbI3c-XRlz4)
"Phase Shift" - Part of “Honkai: Star Rail - Allegory of the Cave (Part 3)” Original Game Soundtrack · Author: HOYO-MIX ℗ 2025 HOYO-MiX
[Phase Shift Youtube link](https://www.youtube.com/watch?v=QH0OmNGUB5w)
"Overflowing Core" - Part of “Honkai: Star Rail - Allegory of the Cave (Part 3)” Original Game Soundtrack · Author: HOYO-MIX ℗ 2025 HOYO-MiX [Overflowing Core Youtube link](https://www.youtube.com/watch?v=2EkUtLTGgVk)
"Virus" - Part of “Honkai: Star Rail - Allegory of the Cave (Part 3)” Original Game Soundtrack · Author: HOYO-MIX ℗ 2025 HOYO-MiX
[Virus Youtube link](https://www.youtube.com/watch?v=bc49K0Rn3nQ)
