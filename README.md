# TFG-Moodle
Repositorio Github del TFG de Alberto Ros Galian

![alt text](https://github.com/albegalia/TFG-Moodle/blob/main/Diagrama%20visual%20TFG.png "Diagrama visual del proyecto")

Este proyecto consiste en la recopilación de eventos generados por Moodle, su análisis para la obtención de datos relevantes tanto para profesores y alumnos, y la representación de dichos datos.

Este está dividido en multiples 'workspaces', por tanto, habrá una carpeta por workspace, y dentro, todos sus archivos correspondientes.

Explicación de lo más relevante a comentar de cada archivo/carpeta:

1. Archivo [docker-compose.yml](https://github.com/albegalia/TFG-Moodle/blob/main/docker-compose.yml)
- Su contenido nos permite tanto instalar e iniciar Moodle y MariaDB. Contiene además las variables de entorno que se usaron para este proyecto.

2. Carpeta [Plugin local](https://github.com/albegalia/TFG-Moodle/tree/main/Plugin%20local)
- Contiene los archivos del plugin local 'send_events'.
- En 'observer.php' se ha omitido tanto la URL del microservicio como su correspondiente token de autorización.

3. Carpeta [Analisis eventos](https://github.com/albegalia/TFG-Moodle/tree/main/Analisis%20eventos)
- Contiene los archivos que se usaron para los análisis de los eventos. 
- Prácticamente todo el trabajo se realizó dentro del archivo de Jupyter Notebook llamado 'tests.ipynb'. Dentro está todo el proceso que se realizó en el análisis de los eventos, además de contener trabajo que no ha terminado en el proyecto final.
- El archivo 'tfg-functions.py' contiene funciones que fui usando para realizar las pruebas, pero al final todo lo he ido realizando dentro de 'tests.ipynb'.
- La carpeta 'square_analytics' fue proporcionada por los directores del proyecto.
- Se ha omitido el archivo '.env', que es el que contenia la cadena de conexión con Azure.

4. Carpeta [Endpoints Azure](https://github.com/albegalia/TFG-Moodle/tree/main/Endpoints%20Azure)
- Contiene los archivos que se usaron para desplegar los endpoints en Azure.
- El archivo que se ocupa de desplegar dichos endpoints es 'function_app.py', que contiene los dos endpoints del proyecto mas uno de prueba que venia por defecto cuando se creó la función Azure en VSCode.
- El archivo 'tfg_functions.py' contiene las funciones que crean la respuesta HTML.
- Se ha omitido el archivo 'local.settings.json', que es el que contenia la cadena de conexión con Azure.

5. Carpeta [Plugins bloque](https://github.com/albegalia/TFG-Moodle/tree/main/Plugins%20bloque)
- Contiene los archivos de los plugins de tipo bloque, 'students_info' y 'teachers_info'.
Se ha omitido el código en la URL que requieren los endpoints para solicitar información tanto en 'block_teachers_info.php' como en 'block_students_info.php'.
