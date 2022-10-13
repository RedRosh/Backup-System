from datetime import datetime
import mimetypes
import smtplib,ssl
from email.message import EmailMessage
import logging

logger = logging.getLogger()
class EmailHandler:
    server = None
    mail_sender = None
        
    def __init__(self,smtp_server,port,mail_sender, password):
        if(EmailHandler.server != None): return
        context = ssl.create_default_context()
        EmailHandler.server = smtplib.SMTP_SSL(smtp_server, port, context=context) 
        EmailHandler.server.login(mail_sender, password)
        EmailHandler.mail_sender = mail_sender
        
    def message_template(self,mail_receivers,subject,body):
        try: 
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = "Archivage Bot" 
            msg['To'] = mail_receivers
            msg.set_content(body)
            filename="archivage_logs_"+ datetime.today().strftime('%Y-%d-%m %H:%M:%S') + '.log'
            path ='/app/logs/logs.log'
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as fp:
                msg.add_attachment(fp.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=filename)
        except Exception as e:
            logger.error(e)                     
        return msg

        
    def send_email(self,mail_receivers,subject,body):
        message = self.message_template(mail_receivers,subject,body)
        EmailHandler.server.send_message(message)
