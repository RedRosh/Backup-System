from datetime import datetime
import mimetypes
import smtplib,ssl
from email.message import EmailMessage
import logging
from modules.ConfigHandler import ConfigHandler

logger = logging.getLogger()
class EmailHandler:
    ''' ##**Cette classe nous permet de manipuler les emails envoyés à l'utilisateur.** '''
    server = None
    ''' cette variable présente notre serveur pour l'envoie du mail. '''
    mail_sender = None
    ''' cette variable est l'envoyeur de notre email, c'est le bot automatisé dans notre cas.'''
        
    def __init__(self,smtp_server,port,mail_sender, password):
        # Applying singleton pattern, to avoid instantiating the class more than once.
        if(EmailHandler.server != None): return
        # create SSL context to add encrypting while sending mails
        context = ssl.create_default_context()
        # connecting to SMTP server
        EmailHandler.server = smtplib.SMTP_SSL(smtp_server, port, context=context) 
        # login to the SMTP server
        EmailHandler.server.login(mail_sender, password)
        EmailHandler.mail_sender = mail_sender
        
    def message_template(self,mail_receivers,subject,body):
        ''' La création du message envoyé et tous ses paramètres.'''
        try: 
            # creating a message object  && init congig handler
            config = ConfigHandler()
            msg = EmailMessage()
            # Setting props
            msg['Subject'] = subject # setting subject
            msg['From'] = "Archivage Bot" # setting sender
            msg['To'] = mail_receivers  # setting receivers
            msg.set_content(body)   # setting body
            # set attachments based on config file
            if config.get_add_attachment() == 1:
                # file name
                filename="archivage_logs_"+ datetime.today().strftime('%Y-%d-%m %H:%M:%S') + '.log'
                # path to the log file
                path ='/app/logs/logs.log'
                # setting up the mimetype based on the extension of the file
                ctype, encoding = mimetypes.guess_type(path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                # adding the attachment to the message
                with open(path, 'rb') as fp:
                    msg.add_attachment(fp.read(),
                                maintype=maintype,
                                subtype=subtype,
                                filename=filename)
        except Exception as e:
            # catching any exception
            logger.error(e)  
        finally:
            # returning the message                                                                                
            return msg

        
    def send_email(self,mail_receivers,subject,body):
        ''' Fonction pour l'envoie de l'email créé. '''
        # creating a message based on message_template function
        message = self.message_template(mail_receivers,subject,body)
        # send message to all mail receivers
        EmailHandler.server.send_message(message)
