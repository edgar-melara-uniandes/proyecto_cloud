from project import create_app
import logging
import sqlalchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .vistas import VistaRegistro, VistaLogin, VistaTasks, VistaTask, VistaFile, HelloWorld, VistaUpdateConverted
from connection_gcp import connect_with_connector
""" from .modelos import db """

app = create_app("default")
logging.basicConfig(level=logging.DEBUG)
app_context = app.app_context()
app_context.push()

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    return connect_with_connector()
    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )
db = None
# init_db lazily instantiates a database connection pool. Users of Cloud Run or
# App Engine may wish to skip this lazy instantiation and connect as soon
# as the function is loaded. This is primarily to help testing.
@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = init_connection_pool()
    
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


jwt = JWTManager(app)

