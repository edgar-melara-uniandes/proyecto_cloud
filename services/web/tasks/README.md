
# Proyecto Cloud - Worker

### Descripción

Instancia con worker y base de datos redis


## Pasos para instancia los componentes en una maquina virtual de GCP

 - crear una maquina virtual en gcp 
 - instalar docker engine
 - ejecutar contenedor de redis con el siguiente comando:
 ```bash
 sudo docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
 ```
 - ejecutar contenedor de worker con el siguiente comando:
 ```bash
sudo docker run -d --name worker-cloud-7 --link redis-stack-server  lsolier/worker-cloud:8.0
 ```
 - verificar que ambos contenedores se encuentran en ejecucion
 ```bash
 sudo docker container ls
 ```
 - Crear una regla de firewall para exponer el puerto 6379, y poder recibir peticiones al worker

