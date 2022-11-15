### Descripción
El objectivo de la applicacion es convertir archivos de audio a diferentes formatos para esto se utilizan las siguientes tecnologias:

- Docker: Se generan imagenos para API Rest, Worker
- Unicorn: Como servidor de la applicacion python que permite la concurrencia de peticiones
- Flask: Para la definición de API rest
- PostgreSQL: Manejador de base de datos, se abstrae con SQLAlchemhy
- Celery: Creación de tareas que se ejecutan de forma asíncrona
- Redis: Para manejar la cola de tareas entregadas por el API
- ffmpeg: Libreria para la conversion de archivos de audio

## Comandos para inicializar app

## API Rest

Debido a las necesidades de autoscaling a través de instance template, todo nodo que quiera montar que use la misma estrategia DEBE usar el script script_inicializacion_apirest.sh al momento de arranque

## Ejecucion de worker

Para ejecutar instancia de worker revisar el siguiente README:

https://github.com/edgar-melara-uniandes/proyecto_cloud/tree/entrega_3/services/web/tasks#readme


## Load Testing

Para ejecutar las pruebas de carga referenciar https://github.com/lsolier/load-testing
