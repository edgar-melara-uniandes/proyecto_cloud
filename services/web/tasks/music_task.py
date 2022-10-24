import os
import time

from celery import Celery
import subprocess
from posixpath import splitext
from pydub import AudioSegment

BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery('music_conversions_batch', backend=BACKEND_URL, broker=BROKER_URL)
UPLOAD_FOLDER = str(os.environ.get("MEDIA_FOLDER", f"{os.getenv('APP_FOLDER')}/project/media"))

@celery_app.task(name='music_conversions')
def add_music_conversion_request(response):

    print("Adding request to queue, musicID: " + str(response['userId']))
    # time.sleep(60)
    convert_audio_file(response)
    #request endpoint de finalizar conversion
    #almacenar_solicitud_bd() or convertir_musica()
    print("After 60 seconds the request was attended")
    return "Music converted :)"

@celery_app.task(name='batch_music_conversion')
def ejecutar_conversion():
    time.sleep(60)
    #convertir_lotes_musica()
    # convert_audio_file(received_file_path,audio_format)
    return "Music converted :)"


def convert_audio_file(response):
    file_name = response['fileName']
    audio_file_path = response['filePath']
    target_format = response['targetType']
    user_id = response['userId']
    task_id = response['taskId']
    
    output = f'{UPLOAD_FOLDER}/{user_id}/{task_id}/converted/{file_name}.{target_format}'

    subprocess.call(["ffmpeg","-i",audio_file_path,output])
    # alternativas:
    # subprocesscall
    # os.system("ffmpeg -i audio_file_a.mp3 audio_file_a.aac") # no recomendado
    
    # pydub; limitaciones por formatos, aunque ffmpeg NO tiene dichas limitaciones
    # sound = AudioSegment.from_file(audio_file_path,"mp3")
    # sound.export(file_name+"_conv.wav", format="wav"), igual en mp3 y ogg
    # excepciones:
    # sound.export(file_name+"_conv.aac", format="adts")
    # sound.export(file_name+"_conv.wma", format="wma") no funciona


