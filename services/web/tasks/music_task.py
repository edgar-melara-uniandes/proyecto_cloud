import os
import time

from celery import Celery
from asyncio import subprocess
from posixpath import splitext
from pydub import AudioSegment

BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery('music_conversions_batch', backend=BACKEND_URL, broker=BROKER_URL)

@celery_app.task(name='music_conversions')
def add_music_conversion_request(music_conversion_json):
    received_file_path = "audio_file_a.mp3"
    audio_format = "aac"
    print("Adding request to queue, musicID: " + str(music_conversion_json['user_id']))
    time.sleep(60)
    # convert_audio_file(received_file_path,audio_format)
    #request endpoint de finalizar conversion
    #almacenar_solicitud_bd() or convertir_musica()
    print("After 60 seconds the request was attended")
    return "Music converted :)"

@celery_app.task(name='batch_music_conversion')
def ejecutar_conversion():
    time.sleep(60)
    #convertir_lotes_musica()
    convert_audio_file(received_file_path,audio_format)
    return "Music converted :)"


def convert_audio_file(audio_file_path, target_format):
    split_up = splitext(audio_file_path)
    file_name = split_up[0]
    file_extension = split_up[1]

    subprocess.run(["ffmpeg","-y","-i",audio_file_path,file_name+"."+target_format])
    # alternativas:
    # subprocesscall
    # os.system("ffmpeg -i audio_file_a.mp3 audio_file_a.aac") # no recomendado
    
    # pydub; limitaciones por formatos, aunque ffmpeg NO tiene dichas limitaciones
    # sound = AudioSegment.from_file(audio_file_path,"mp3")
    # sound.export(file_name+"_conv.wav", format="wav"), igual en mp3 y ogg
    # excepciones:
    # sound.export(file_name+"_conv.aac", format="adts")
    # sound.export(file_name+"_conv.wma", format="wma") no funciona


