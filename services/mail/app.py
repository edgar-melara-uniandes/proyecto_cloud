from flask import Flask
from flask_mail import Mail, Message
# import os

app = Flask(__name__)

# os.environ.get('MY_ENVIRONMENT_VARIABLE') # trae variable de entorno MY_ENVIRONMENT_VARIABLE

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587 # 465 si SSL, ajustar los MAIL_USE_* como corresponda
app.config['MAIL_USERNAME'] = "putAMailHere@amail.net"  # Correo remitente
app.config['MAIL_PASSWORD'] = "putPasswordHere" # en caso de GMail, usar un app password (requiere habilitar 2FA)
app.config['MAIL_USE_TLS'] = True # habilita protocolo TLS, setear SSL a false si se usa
app.config['MAIL_USE_SSL'] = False # habilita protocolo SSL, setear TLS a false si se usa
mail = Mail(app)

@app.route('/')
def message_route():
    sender = "putAMailHere@amail.net" # Correo remitente
    receivers = ['c.toros@unianndes.edu.co'] # poner destinatario(s) aca
    subject = 'Tarea de conversión finalizada' # Asunto
    message = Message(subject, sender = sender, recipients = receivers)
    message.body = "Tarea de conversión terminada para xxxx.file a formato .target, puede descargar el archivo"
    mail.send(message)
    return "Finished", 200