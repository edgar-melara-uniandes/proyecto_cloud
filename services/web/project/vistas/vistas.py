import sys
import os
import shutil
import uuid
import datetime
from google.cloud import storage
from celery import Celery
from celery.result import AsyncResult
from flask_restful import Resource
from flask import request, send_file, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from project.modelos import db, Appuser, Task, AppuserSchema, TaskSchema
from project.vistas.cloud_storage_client import CloudStorageClient

load_dotenv() 

user_schema = AppuserSchema()
task_schema = TaskSchema()
list_task_schema = TaskSchema(many=True)
UPLOAD_FOLDER = str(os.environ.get("MEDIA_FOLDER", f"{os.getenv('APP_FOLDER', '/usr/src/app')}/tmp"))
BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery('music_conversions_batch', backend=BACKEND_URL, broker=BROKER_URL)
cloud_storage_client = CloudStorageClient()

@celery_app.task(name = 'music_conversions')
def add_music_conversion_request(music_conversion):
    pass

ALLOWED_EXTENSIONS = {"mp3", "acc", "ogg", "wav","wma"}
class VistaRegistro(Resource):

    def post(self):
        usuario_viejo = Appuser.query.filter(Appuser.username == request.json["username"]).first()
        email_viejo = Appuser.query.filter(Appuser.email == request.json["email"]).first()
        if usuario_viejo is not None or email_viejo is not None:
            return {"mensaje": "El usuario o correo electronico ya estan registrados", "status": "fail"}, 404
        if request.json['password1'] != request.json['password2']:
            return {"mensaje": "Las contraseñas deben ser iguales", "status": "fail"}, 404
        
        nuevo_usuario = Appuser(username=request.json['username'], email=request.json['email'], password=request.json['password1'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity=nuevo_usuario.id)
        return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "status": "success", "id": nuevo_usuario.id}

class VistaLogin(Resource):

    def post(self):
        usuario = Appuser.query.filter(Appuser.username == request.json["username"],
                                       Appuser.password == request.json["password"]).first()
        db.session.commit()
        if usuario is None:
            return {"mensaje": "Revise los datos e intente nuevamente", "status": "fail"}, 404
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "status": "success"}

class VistaTasks(Resource):

       
    @jwt_required()
    def get(self):
        params = request.args
        max = params.get('max', default="", type=str)
        order = params.get('order', default=None, type=str)
        identity = get_jwt_identity()
        tasks = Task.query.filter(Task.id_user == identity)
        if order != None:
            if order == "1":
                tasks = tasks.order_by(Task.id.desc())
            elif order == "0":
                tasks = tasks.order_by(Task.id.asc())
                
        if max != "":
            tasks = tasks.limit(max)
            
         
        return list_task_schema.dump(tasks)
    
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        folder = uuid.uuid4()
        if 'fileName' not in request.files:
            return {"message": "cargar un archivo en fileName", "status":"fail"}, 404
        if request.files == '':
            return {"message": "cargar un archivo en fileName", "status":"fail"}, 404
        if not request.form.get("newFormat"):
            return {"message": "Debe agregar el formato de destino", "status":"fail"}, 404
        process_upload_file = uploadFile(request.files, identity, folder)
        if process_upload_file['status'] is True:
            new_task = Task(date_created=datetime.datetime.now(),format_input=process_upload_file["format_input"], format_output=request.form.get("newFormat"), path_input=process_upload_file["file_path"], status="uploaded", id_user=identity, folder = str(folder), file_name=process_upload_file['file_name'])
            db.session.add(new_task)
            db.session.commit()
            data = {
                    "userId": identity,
                    "filePath": new_task.path_input,
                    "originType": new_task.format_input,
                    "targetType": new_task.format_output, 
                    "taskId": new_task.folder,
                    "fileName": new_task.file_name.replace(" ", "_"),
                    "formatInput": new_task.format_input                    
                }
            args = (data,)
            task = add_music_conversion_request.apply_async(args)
            return {"message": "El archivo fue cargado y la tarea creada", "status":"success"}
        return {"message": "Problemas cargando el archivo", "status":"fail"}, 404
        
class VistaTask(Resource): 
    @jwt_required()
    def get(self, id_task):
        identity = get_jwt_identity()
        task = Task.query.filter(Task.id == id_task, Task.id_user == identity).one_or_none()
        if task is None:
            return {"message": "No se encontro la tarea"}
        return task_schema.dump(task)
    @jwt_required()
    def put(self, id_task):
        identity = get_jwt_identity()
        if not request.form.get("newFormat"):
            return {"message": "Debe agregar el formato de destino", "status":"fail"}, 404
        if not request.form.get("newFormat") in ALLOWED_EXTENSIONS:
            return {"message": "El formato no es válido", "status":"fail"}, 404
        task = Task.query.filter(Task.id == id_task, Task.id_user == identity).one_or_none()
        if task is None:
            return {"message": "No se encontro la tarea"}
        if task.path_output != None:
            """borrado cloud storage"""
            cloud_storage_client.delete_blob(task.path_output)
        task.format_output = request.form.get("newFormat")
        task.status = "uploaded"
        task.date_updated=datetime.datetime.now()
        task.path_output = None
        db.session.commit()
        return task_schema.dump(task)
    @jwt_required()
    def delete(self, id_task):
        identity = get_jwt_identity()
        task = Task.query.filter(Task.id == id_task, Task.id_user == identity).one_or_none()
        if task is None:
            return {"message": "No se encontro la tarea"}
        if task.path_input != None:
            """Borrado de cloud storage"""
            cloud_storage_client.delete_folder(str(identity) + "/" + task.folder)
        db.session.delete(task)
        db.session.commit()
        return {"message": "La tarea ha sido eliminada", "status": "success"}, 204
    
class VistaMedia(Resource): 
    def get(self, filename):
        return send_from_directory(UPLOAD_FOLDER, filename)   
class VistaFile(Resource):
    @jwt_required()
    def get(self, filename):
        identity = get_jwt_identity()
        task = Task.query.filter(Task.file_name == filename, Task.id_user == identity).one_or_none()
        if task is None:
            return {"message": "No se encontro la tarea"}
        if task.path_output != None:
            return send_file(task.path_output, as_attachment=True)  
        else:
            """ mimetype="application/octet-stream", """
            return send_file(task.path_input,  as_attachment=True) 
class VistaUpdateConverted(Resource):
    def post(self):
        task = Task.query.filter(Task.folder == request.json['taskId']).one_or_none()
        if task is None:
            return {"message": "No se encontro la tarea", "status": "fail"}, 404
        task.path_output = request.json['output']
        task.date_updated = datetime.datetime.now()
        task.status = "processed"
        db.session.commit()
        return {"message": "Actualización realizada", "status": "success"}, 200
class HelloWorld(Resource):
    def get(self):
        return {"hello":"world"}, 200

def uploadFile(files, identity, folder):
    response = dict()
    file = files['fileName']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_task = str(UPLOAD_FOLDER + "/" + str(folder)) 
        if not os.path.exists(path_task): # cambiar
            os.makedirs(path_task)
        destination_blob_name = f'{identity}/{folder}/upload/{filename}'
        tmp_file = os.path.join(path_task, filename)
        """Guarda archivo en tmp"""
        file.save(tmp_file)
        """CloudStorage""" 
        cloud_storage_client.upload_file(tmp_file, destination_blob_name)
        cloud_storage_client.verify_if_file_exist(destination_blob_name)
        file_path = destination_blob_name
        response["status"] = True 
        response["file_path"] = file_path
        response["format_input"] = file.filename.rsplit('.', 1)[1].lower()
        response["file_name"] = file.filename.rsplit('.', 1)[0].lower()
        shutil.rmtree(path_task)
    else:
        response["status"] = False
    return response
         
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def listToString(s):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += ele
 
    # return string
    return str1 