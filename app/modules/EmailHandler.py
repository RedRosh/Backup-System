import smtplib,ssl
from email.message import EmailMessage

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
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = "Archivage Bot" 
        msg['To'] = mail_receivers
        msg.set_content(body)
        return msg

        
    def send_email(self,mail_receivers,subject,body):
        message = self.message_template(mail_receivers,subject,body)
        EmailHandler.server.send_message(message)
