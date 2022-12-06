
# Proyecto Cloud - Worker

### Descripción

Instancia Worker basada en Google App Engine

## Pasos para instancia el worker en una maquina virtual de GCP

- Activar App Engine API en un proyecto GCP

- Descargar contenido del repositorio y apuntar a esta carpeta:

- Actualizar contenido de `worker-service.yaml`, reemplazando por los valores de variables de entorno correctos. Guardar.

- Sea desde Cloud Shell o desde una máquina con Google Cloud SDK Shell instalado, correr el siguiente comando (requiere un servicio default ya desplegado en App Engine):
`gcloud app deploy worker-service.yaml`

Esto toma varios minutos, en especial durante el primer despliegue

 #### *Opcional
 - Ahora si publica mensajes en el topico creado para el proyecto (converter-topic) puede crear tareas de encolado

