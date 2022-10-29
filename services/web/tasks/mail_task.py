from email.message import EmailMessage
import smtplib

import smtplib

def send_mail(file_name, target_format, task_id):
    # os.environ.get('MY_ENVIRONMENT_VARIABLE') # trae variable de entorno MY_ENVIRONMENT_VARIABLE
    try:
        sender = "putAMailHere@amail.net" # Correo remitente
        receivers = ['c.toros@unianndes.edu.co'] # poner destinatario(s) aca

        message = EmailMessage()
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = "Tarea de conversión finalizada"
        message.set_content("Tarea de conversión con ID " + task_id + " para " + file_name + " a formato " + target_format
                      + " terminada. Puede descargar el archivo!")
        #message.set_content("Tarea de conversión terminada para xxxx.file a formato .target, puede descargar el archivo")

        smtp= smtplib.SMTP('smtp.gmail.com', 587) # smtplib.SMTP_SSL('smtp.gmail.com', 465) alternativa, menos seguro SSL que TLS
        smtp.ehlo()
        smtp.starttls() # requerido en modo TLS
        smtp.login(sender, "putPasswordHere") # en caso de GMail, usar un app password (requiere habilitar 2FA)
        smtp.send_message(message)
    except Exception as e:
        print("Error al enviar correo")
        print(str(e))
    

send_mail("audio_sample.mp3", "MP3", "abcde123")