import os
import time
#import requests
import json
import uuid
import tasks.util as Util
import datetime

from celery import Celery
import subprocess
from posixpath import splitext
from pydub import AudioSegment
from tasks.cloud_storage_client import CloudStorageClient
from tasks.modelos import db, Task

BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery('music_conversions_batch', backend=BACKEND_URL, broker=BROKER_URL)
UPLOAD_FOLDER = str(os.environ.get("MEDIA_FOLDER", f"{os.getenv('APP_FOLDER')}/project/media"))
ENDPOINT = str(os.environ.get("ENDPOINT_CONVERTED_DB", "http://127.0.0.1:1337/api/converted"))

@celery_app.task(name='music_conversions')
def add_music_conversion_request(response):
    print("Adding request to queue, musicID: " + str(response['userId']))
    convert_audio_file(response)
    print("After 60 seconds the request was attended")
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
    
    output = f'{temp_path}/converted/{file_name}.{target_format}'
    destination_blob_name = f'{user_id}/{task_id}/converted/{file_name}.{target_format}'

    try:
        #convertir
        subprocess.call(["ffmpeg","-i", temporal_file_destination, output])
    except:
        print("Error publishing file in cloud storage")
        pass
    else:
        cloud_storage_client.upload_file(output, destination_blob_name)
        cloud_storage_client.verify_if_file_exist(destination_blob_name)
        updated_db(task_id, output)
        Util.delete_temporal_path(temp_path)
    # alternativas:
    # subprocesscall
    # os.system("ffmpeg -i audio_file_a.mp3 audio_file_a.aac") # no recomendado
    
    # pydub; limitaciones por formatos, aunque ffmpeg NO tiene dichas limitaciones
    # sound = AudioSegment.from_file(audio_file_path,"mp3")
    # sound.export(file_name+"_conv.wav", format="wav"), igual en mp3 y ogg
    # excepciones:
    # sound.export(file_name+"_conv.aac", format="adts")
    # sound.export(file_name+"_conv.wma", format="wma") no funciona

def updated_db(taskId, output):
    task = Task.query.filter(Task.folder == taskId).one_or_none()
    if task is None:
        return {"message": "No se encontro la tarea", "status": "fail"}, 404
    task.path_output = output
    task.date_updated = datetime.datetime.now()
    task.status = "processed"
    db.session.commit()
    return {"message": "Actualización realizada", "status": "success"}, 200
    # send = {"taskId":taskId, "output": output}
    # headers = {'Content-Type': 'application/json'}
    # result = requests.post(ENDPOINT,data=json.dumps(send),headers=headers)
    # print(result.content)
