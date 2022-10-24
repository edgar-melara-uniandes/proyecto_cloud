import os
import time

from celery import Celery

BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery('music_conversions_batch', backend=BACKEND_URL, broker=BROKER_URL)

@celery_app.task(name='music_conversions')
def add_music_conversion_request(music_conversion_json):
    print("Adding request to queue, musicID: " + str(music_conversion_json['music_id']))
    time.sleep(60)
    #almacenar_solicitud_bd() or convertir_musica()
    print("After 60 seconds the request was attended")
    return "Music converted :)"

@celery_app.task(name='batch_music_conversion')
def ejecutar_conversion():
    time.sleep(60)
    #convertir_lotes_musica()
    return "Music converted :)"