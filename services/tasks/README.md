
# Proyecto Cloud - Worker

### Descripción

Instancia Worker migrada a Google Cloud Pub/Sub, suscriptor


## Pasos para instancia el worker en una maquina virtual de GCP

 - Crear una máquina virtual en GCP
 - Instalar docker engine
 ```bash
 https://docs.docker.com/engine/install/ubuntu/
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
sudo docker run -e BUCKET_NAME=music-converter-prueba-1 -e GOOGLE_APPLICATION_CREDENTIALS=/credential/service-account/<service-account-json> -e DATABASE_URL=<url-database> -e ENABLED_EMAIL=false -e GCP_PROJECT_NAME=devopslsolier -e TARGET_SUBSCRIPTION=converter-topic-sub -d --name worker-cloud-prod-pub-sub -v $(pwd)/service-account:/credential/service-account lsolier/worker-cloud-pub-sub:latest
 ```
 - verificar que ambos contenedores se encuentran en ejecucion
 ```bash
 sudo docker container ls
 ```
 
 #### *Opcional
 - Ahora si publica mensajes en el topico creado para el proyecto (converter-topic) puede crear tareas de encolado

