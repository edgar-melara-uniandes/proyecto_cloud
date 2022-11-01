
# Proyecto Cloud - Conversión formatos de Audio

### Descripción
El objectivo de la applicacion es convertir archivos de audio a diferentes formatos para esto se utilzan las siguientes tecnologias:

- Docker: para la orquestacion de los servicios, contenedores donde se ejecutan las diferentes componentes de la aplicación
- Nginx: Como revese proxy, enmascara al cliente los servicios expuestos
- Unicorn: Como servidor de la applicacion python que permite la concurrencia de peticiones
- Flask: Para la definon de API rest
- Postgres: Manejador de base de datos
- Celery: Creacion de tareas que se ejecutan de forma asincrona
- Redis: Para manejar la cola de tareas entregadas por el API
- FFMPEG: Libreria para la conversion de archivos de audio



## Comandos para inicializar Api-Rest en Compute Engine de GCP
El pre requisito es tener una instancia de Compute Engine con ubuntu con las siguientes instalaciones:
- Python 3.8 o superior
- Docker (https://docs.docker.com/engine/install/ubuntu/)
- Docker Compose
- Git

### Comandos para ejecucion:

1. Descargar repositorio:
  ```bash
    git clone https://github.com/edgar-melara-uniandes/proyecto_cloud.git
  ```
2. Iniciar la ejecucion de los contenedores de NGINX y API-REST:
  ```bash
    sudo docker-compose -f docker-compose-cloud.prod.yml up -d --build
  ```
3.  Para detener la aplicación es necesario, ejecutar el comando siguiente

```bash 
  sudo docker-compose -f docker-compose.prod.yml down -v
  ```

4. Si es necesario acceder a la base de datos podemos ejecutar el comando

```bash
  sudo docker-compose exec db psql --username=postgres --dbname=conversion_prod
```

## Comandos para inicializar app LOCAL
El prerequisito para ejecutar el app es, tener docker previamente instalado

Para inicializar la aplicación se ejecuta el comando:

```bash
  docker-compose -f docker-compose.prod.yml up -d --build
```
para que funcione en consola se tiene que estar en la ruta base el proyecto al mismo nivel del archivo `docker-compose.prod`

Para detener la aplicación es necesario, ejecutar el comando siguiente

```bash 
  docker-compose -f docker-compose.prod.yml down -v
  ```

Si es necesario acceder a la base de datos podemos ejecutar el comando

```bash
  docker-compose exec db psql --username=postgres --dbname=conversion_prod
```
Para ejecutar las pruebas de carga referenciar https://github.com/edgar-melara-uniandes/proyecto_cloud/blob/main/services/test/README.md
