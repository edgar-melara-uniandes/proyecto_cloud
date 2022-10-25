
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




## Comandos para inicializar app
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
