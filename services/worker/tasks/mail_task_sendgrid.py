from email.message import EmailMessage
import smtplib
import os


def send_mail(file_name, target_format, task_id):
    sak = os.environ.get('SENDGRID_API_KEY')
    try:
        sender = "c.toros.uniandes@gmail.com" # Correo remitente con sendgrid
        receivers = ['c.toros@uniandes.edu.co'] # poner destinatario(s) aca

        message = EmailMessage()
        message['From'] = sender
        message['To'] = receivers
        message['Subject'] = "Tarea de conversión finalizada"
        message.set_content("Tarea de conversión con ID " + task_id + " para " + file_name + " a formato " + target_format
                      + " terminada. Puede descargar el archivo!")
        

        smtp= smtplib.SMTP('smtp.sendgrid.net', 587) # smtplib.SMTP_SSL('smtp.gmail.com', 465) alternativa, menos seguro SSL que TLS
        smtp.ehlo()
        smtp.starttls() # requerido en modo TLS
        smtp.login('apikey', sak)
        smtp.send_message(message)
    except Exception as e:
        print("Error al enviar correo")
        print(str(e))
    