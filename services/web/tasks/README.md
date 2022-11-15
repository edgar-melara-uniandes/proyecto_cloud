
# Proyecto Cloud - Worker

### Descripción

Instancia worker con celery y base de datos redis


## Pasos para instancia el worker en una maquina virtual de GCP

 - crear una maquina virtual en gcp 
 - instalar docker engine
 ```bash
 https://docs.docker.com/engine/install/ubuntu/
 ```
 - ejecutar contenedor de redis con el siguiente comando:
 ```bash
 sudo docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
 ```
 - ejecutar contenedor de worker con el siguiente comando:

 crear carpeta /service-account y agregar dentro de dicha carpeta el arhcivo json que representa al service account:

 ```bash
 mkdir service-account
 ```


Ejecutar el siguiente comando docker:

 - Para envío de correo habilitado:
 ```bash
sudo docker run -e BUCKET_NAME=music-converter-prueba-1 -e GOOGLE_APPLICATION_CREDENTIALS=/credential/service-account/<service-account-json> -e DATABASE_URL=<url-database> -e ENABLED_EMAIL=true SENDGRID_API_KEY=<your_sendgrid_api_key> -d --name worker-cloud-prod -v $(pwd)/service-account:/credential/service-account --link redis-stack-server  lsolier/worker-cloud:latest
 ```
 - Para envío de correo deshabilitado:
 ```bash
sudo docker run -e BUCKET_NAME=music-converter-prueba-1 -e GOOGLE_APPLICATION_CREDENTIALS=/credential/service-account/<ruta-de-service-account-json> -e DATABASE_URL=<url-database> -e ENABLED_EMAIL=false -d --name worker-cloud-prod -v $(pwd)/service-account:/credential/service-account --link redis-stack-server  lsolier/worker-cloud:latest
 ```
 - verificar que ambos contenedores se encuentran en ejecucion
 ```bash
 sudo docker container ls
 ```
 
 #### *Opcional
 - Si desea acceder al worker desde una red externa debe crear una regla de firewall para exponer el puerto 6379, y poder recibir peticiones.

