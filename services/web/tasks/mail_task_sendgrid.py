from email.message import EmailMessage
import smtplib
import os

def send_mail(file_name, target_format, task_id):
    sendgrid_user = os.environ.get('SENDGRID_USER') # trae variable de entorno MY_ENVIRONMENT_VARIABLE
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY') # trae variable de entorno MY_ENVIRONMENT_VARIABLE
    try:
        sender = sendgrid_user # Correo remitente con sendgrid
        receivers = ['c.toros@unianndes.edu.co'] # poner destinatario(s) aca

        message = EmailMessage()
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = "Tarea de conversión finalizada"
        message.set_content("Tarea de conversión con ID " + task_id + " para " + file_name + " a formato " + target_format
                      + " terminada. Puede descargar el archivo!")
        #message.set_content("Tarea de conversión terminada para xxxx.file a formato .target, puede descargar el archivo")

        smtp= smtplib.SMTP('smtp.sendgrid.net', 587) # smtplib.SMTP_SSL('smtp.gmail.com', 465) alternativa, menos seguro SSL que TLS
        smtp.ehlo()
        smtp.starttls() # requerido en modo TLS
        smtp.login('apikey', sendgrid_api_key) # en caso de GMail, usar un app password (requiere habilitar 2FA)
        smtp.send_message(message)
    except Exception as e:
        print("Error al enviar correo")
        print(str(e))
    