import ftplib
from io import BytesIO
from modules.ConfigHandler import ConfigHandler
from modules.DbHandler import DbHandler
from os import environ
from datetime import date, timedelta
import logging

logger = logging.getLogger()

class ServerDistant:
    '''##**Pour gérer le serveur distant.**'''
    
    session=None
    '''La variable qui constitue une session du serveur distant.'''

    def __init__(self,server_address,username,password):
        '''Initialisation de la session.'''
        # We are using the ftplib library to connect to the FTP server.
        self.session=ftplib.FTP(server_address,username,password)
        logger.info("Connection to distant server was established.")
    
    
    def add_file(self,file,hash):
        '''Manipulation des fichiers Ajoutés ou déjà existants selon des critères bien définis qui concernent *l'historisation*, ceci est expliqué par le tableau suivant :

        |     | Historisation : False     | Historisation : True | 
        | :---:   | :-----------: | :---: |
        |     | -----   | ----- |
        | **ficher existant** | on étend le délai d'expiration et on supprime le reste | on étend le délai d'expiration |
        |  -----   | -----   | ----- |
        | **nouveau fichier** | on supprime tout et on ajoute  | on ajoute simplement  |

        '''
        # This function is used to add a file to the distant server.
        # init the config handler && DbHandler
        config = ConfigHandler()
        db=  DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
        # Getting the expiration date && versioning.
        expiration_date =  date.today() + timedelta(days=  int(config.get_expired_in()))
        versioning = bool(int(config.get_versioning()))
        logger.info('Versioning is {}.'.format( "enabled" if versioning else "disabled"))
        # fetching All Valid records
        records =  db.find_record(hash)
        # applying different rules according to the status of versioning.
        if  versioning:
            if len(records) ==0:
                logger.info("File does not exist in FTP.")
                
                self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue())) # adding file to the distant server.
                db.add_record(hash,expiration_date,file.filename) # adding record to the database
                logger.info("File was added successfully.")
            else:
                logger.info("File does exist in FTP.")
                db.update_record(hash,True,expiration_date) # extending the expiration date
                logger.info("The expiration date of the file was extended.")
        else:
            if len(records) == 0:
                logger.info("File does not exist in FTP.")
                db.update_all() # updating all records to be invalid.
                logger.info("Deleting pre-existing files.") 
                self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue()))  # adding file to the distant server.
                db.add_record(hash,expiration_date,file.filename)   # adding record to the database
                logger.info("File was added successfully.")
            else:
                logger.info("File does exist in FTP.")
                db.update_all(records[0][1])  # Deleting all files except the current one.
                logger.info("Deleting pre-existing files.") 
                db.update_record(hash,True,expiration_date)   # extending the expiration date
                logger.info("The expiration date of the file was extended.")

         
    def delete_file(self,filename):
        '''Suppression du fichier.'''
        # Deleting the file from the distant server.
        self.session.delete(filename)
    
    def close_connection(self):
        '''Pour se déconnecter.'''
        # Closing the connection to the distant server.
        self.session.quit()
