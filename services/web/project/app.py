from project import create_app
import logging
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .vistas import VistaRegistro, VistaLogin, VistaTasks, VistaTask, VistaFile, HelloWorld, VistaUpdateConverted, VistaMedia
from .modelos import db

app = create_app("default")
logging.basicConfig(level=logging.DEBUG)
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
cors = CORS(app)


api = Api(app)
api.add_resource(HelloWorld,'/')
api.add_resource(VistaRegistro,'/api/auth/signup')
api.add_resource(VistaLogin,'/api/auth/login')
api.add_resource(VistaTasks,'/api/tasks')
api.add_resource(VistaTask,'/api/tasks/<int:id_task>')
api.add_resource(VistaFile,'/api/files/<string:filename>')
api.add_resource(VistaUpdateConverted,'/api/converted')
api.add_resource(VistaMedia, "/media/<path:filename>")


jwt = JWTManager(app)

