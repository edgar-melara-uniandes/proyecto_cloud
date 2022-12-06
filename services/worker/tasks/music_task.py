import os
import uuid
import tasks.util as Util
import datetime
import json
import tasks.mail_task_sendgrid as SengridMail

import subprocess
from posixpath import splitext
from tasks.cloud_storage_client import CloudStorageClient
from google.cloud import pubsub_v1
from tasks.modelos import Task

import tasks.db as db

UPLOAD_FOLDER = str(os.environ.get("MEDIA_FOLDER", f"{os.getenv('APP_FOLDER')}/project/media"))
ENDPOINT = str(os.environ.get("ENDPOINT_CONVERTED_DB", "http://127.0.0.1:1337/api/converted"))
ENABLED_EMAIL = os.environ.get('ENABLED_EMAIL', 'false')
GCP_PROJECT_NAME = os.environ.get("GCP_PROJECT_NAME", "nombre-proyecto")
TARGET_SUBSCRIPTION = os.environ.get("TARGET_SUBSCRIPTION", "converter-topic-sub")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(GCP_PROJECT_NAME, TARGET_SUBSCRIPTION)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    
    msg = message.data.decode('utf-8')

    decoded_message = json.loads(msg)
    print("Adding request to queue, musicID: " + str(decoded_message['userId']))
    convert_audio_file(decoded_message)
    message.ack()
    return "Music converted :)"

def convert_audio_file(response):
    file_name = response['fileName'] #nombre archivo sin extension
    format_input = response['formatInput'] #extension
    audio_file_path = response['filePath'] #ruta en storage
    target_format = response['targetType'] #formato a convertir
    user_id = response['userId']
    task_id = response['taskId']

    temp_path = str(uuid.uuid4())
    temporal_file_destination = Util.create_temporal_file_destination(temp_path, file_name, format_input)

    cloud_storage_client = CloudStorageClient()
    cloud_storage_client.download_file(audio_file_path, temporal_file_destination)
    
    output = f'{temp_path}/{file_name}.{target_format}'
    
    try:
        subprocess.call(["ffmpeg","-i", temporal_file_destination, output,"-y"])
        if os.path.exists(output):
            print(f"Archivo convertido exitosamente en: {output}")
        else:
            print("Archivo no se llego a crear")
    except Exception as e:
        print("ERRORRRR=====> " + e)
        print("Error publishing file in cloud storage")
        pass
    else:
        destination_blob_name = f'{user_id}/{task_id}/converted/{file_name}.{target_format}'
        cloud_storage_client.upload_file(output, destination_blob_name)
        cloud_storage_client.verify_if_file_exist(destination_blob_name)
        db_response = updated_db(task_id, destination_blob_name)
        print(db_response)
        Util.delete_temporal_path(temp_path)
        if ENABLED_EMAIL == "true":
           SengridMail.send_mail(f'{file_name}.{format_input}', target_format, task_id)


def updated_db(taskId, destination_blob_name):
    task = db.session.query(Task).filter(Task.folder == taskId).one_or_none()
    if task is None:
        return {"message": "No se encontro la tarea", "status": "fail"}
    task.path_output = destination_blob_name
    task.date_updated = datetime.datetime.now()
    task.status = "processed"
    db.session.commit()
    return {"message": "Actualización realizada", "status": "success"}
    
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        print("Listening for messages...")
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        # streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()
        print("coreend")
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.