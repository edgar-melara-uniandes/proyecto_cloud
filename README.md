
# Proyecto Cloud - Conversión formatos de Audio

### Descripción










## Comandos para inicializar app


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
