### Descripción
El objectivo de la applicacion es convertir archivos de audio a diferentes formatos para esto se utilizan las siguientes tecnologias:

- Docker: Se generan imágenes para API Rest, Worker
- Unicorn: Como servidor de la applicacion Python que permite la concurrencia de peticiones
- Flask: Para la definición de API REST
- PostgreSQL: Manejador de base de datos, se abstrae con SQLAlchemhy
- Google Cloud Pub/Sub: Para encolado de tareas de conversión a modo de mensajes, entregadas por el API
- ffmpeg: Librería para la conversion de archivos de audio

## Comandos para inicializar app

## API REST

Debido a las necesidades de autoscaling a través de instance template, todo nodo que quiera montar que use la misma estrategia DEBE usar el script script_inicializacion_apirest.sh al momento de arranque

## Ejecucion de worker

Para ejecutar instancia de worker revisar el siguiente README:

https://github.com/edgar-melara-uniandes/proyecto_cloud/tree/entrega_4/services/web/tasks#readme


## Load Testing

Para ejecutar las pruebas de carga referenciar https://github.com/lsolier/load-testing
