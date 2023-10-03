import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class SendMail:
    smtp_server = ''
    smtp_port = 587
    smtp_username = ''
    smtp_password = ''

    sender_email = ''
    receiver_email = []

    # Asunto y mensaje del correo electrónico
    subject = 'Confirmación: Correo Electrónico de Prueba desde Python - Envío de Clave de Encriptación'
    message = f'Hola,\n\nEspero que este mensaje te encuentre bien. Este correo electrónico es una prueba enviada desde Python para demostrar el envío automático de mensajes. En este caso, estamos enviando la clave de encriptación de los archivos. ¡Que tengas un buen día!\n\n'

    def __init__(self, key):
        self.message = self.message + 'Clave:  '+ key +'  \n\n'
        self.message = self.message + 'Atentamente,\n  \n\n'

        print(self.message)
        pass
    
    def send_email_zoho(self, file_to_attach=None):
        # Crea un objeto MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(self.receiver_email) 
        msg['Subject'] = self.subject

        # Agrega el mensaje al cuerpo del correo
        msg.attach(MIMEText(self.message, 'plain'))

        if file_to_attach:
            # Adjunta el archivo al correo electrónico
            attachment = open(file_to_attach, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file_to_attach}')
            msg.attach(part)

        # Inicia la conexión con el servidor SMTP de Zoho Mail
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            
            # Envía el correo electrónico
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())

        print('Correo electrónico enviado con éxito.')
