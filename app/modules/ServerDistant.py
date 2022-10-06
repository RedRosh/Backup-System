import ftplib
from io import BytesIO
from modules.ConfigHandler import ConfigHandler
from modules.DbHandler import DbHandler
from os import environ
from datetime import date, timedelta


class ServerDistant:
    '''##**Pour gérer le serveur distant.**'''
    
    session=None
    '''La variable qui constitue une session du serveur distant.'''

    def __init__(self,server_address,username,password):
        self.session=ftplib.FTP(server_address,username,password)
    
    
    def add_file(self,file,hash):
        '''Manipulation des fichiers Ajoutés ou déjà existants selon des critères bien définis qui concernent *l'historisation*, ceci est expliqué par le tableau suivant :

        |     | False     | True | 
        | :---:   | :-----------: | :---: |
        |     | -----   | ----- |
        | ficher existant | on étend le délai l'expiration et on supprime le reste | on ajoute |
        |  -----   | -----   | ----- |
        | nouveau fichier | on supprime tout et on rajoute  | on étend le délai d"expiration |

        '''
        config = ConfigHandler()
        db=  DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
        expiration_date =  date.today() + timedelta(days=  int(config.get_expired_in()))
        versioning = bool(int(config.get_versioning()))
        
        records =  db.find_record(hash)
        if  versioning:
            if len(records) ==0:
                self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue()))
                db.add_record(hash,expiration_date,file.filename)
            else:
                db.update_record(hash,True,expiration_date)
        else:
            if len(records) == 0:
                db.update_all()
                self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue()))
                db.add_record(hash,expiration_date,file.filename)
            else:
                db.update_all(records[0][1])  
                db.update_record(hash,True,expiration_date)

        db.close_connection()
         
    def delete_file(self,filename):
        '''Suppression du fichier.'''
        self.session.delete(filename)
    
    def close_connection(self):
        '''Pour se déconnecter.'''
        self.session.quit()
