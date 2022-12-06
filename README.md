### Descripción
El objectivo de la applicacion es convertir archivos de audio a diferentes formatos para esto se utilizan las siguientes tecnologias:

- **Docker:** Se generan imágenes para API Rest, Worker
- **GUnicorn:** Como servidor de la applicacion Python que permite la concurrencia de peticiones
- **Flask:** Para la definición de API REST
- **Google Cloud SQL(PostgreSQL):** Servicio de GCP para el manejo de instancias de bases de datos, allí se persiste la información de la aplicación
- **Google Cloud Pub/Sub:** Para encolado de tareas de conversión a modo de mensajes, entregadas por el API
- **Google Cloud App Engine:** Servicio PaaS proporcionado por GCP para el despliege del ```Api-Rest``` y ```Worker``` 
- **ffmpeg:** Librería para la conversion de archivos de audio

## Comandos para inicializar app

### API REST

Para desplegar el ```Api-Rest``` en Google Cloud App Engine debe ingresar al directorio:
```bash
$ cd services/web
```
Una vez se encuentre en el directorio debe crear un archivo con el nombre **app.yaml**
```bash
nano app.yaml
```
Copiar y **[Completar]** la siguiente información:
```yaml
runtime: python

env: flex
runtime_config:
    python_version: 3.7

entrypoint: gunicorn -b :8080 manage:app

env_variables:
    DATABASE_URL: "[Completar]"
    FLASK_APP: "[Completar]"
    FLASK_DEBUG: "[Completar]"
    SQL_HOST: "[Completar]"
    SQL_PORT: "[Completar]"
    DATABASE: "[Completar]"
    SECRET_KEY: "[Completar]"
    GCP_PROJECT_NAME: "[Completar]"
    TARGET_TOPIC: "[Completar]"
    BUCKET_NAME: "[Completar]"

automatic_scaling:
    max_num_instances: 1
```
Despues de haber guardado el archivo puede ejecutar el siguiente comando haciendo uso de **Google Cloud CLI**
```bash
gcloud app deploy
```

El proceso puede llevar unos minutos en ejecutarse.

### Ejecucion de worker

Para ejecutar instancia de worker revisar el siguiente README:

https://github.com/edgar-melara-uniandes/proyecto_cloud/tree/entrega_5/services/web/tasks#readme


### Load Testing

Para ejecutar las pruebas de carga referenciar https://github.com/lsolier/load-testing
