import ftplib
from io import BytesIO
from FileManager import FileManager
from DbHandler import DbHandler
from os import environ

class ServerDistant:
    
    session=None

    def __init__(self,server_address,username,password):
        self.session=ftplib.FTP(server_address,username,password)
    
    def add_file(self,file):
        db=  DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
        hash= FileManager.get_hash(file)
        filename = file.filename
        expiration_date = '2022-01-01'
        db.add_record(hash,expiration_date,filename)
        self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue()))

    
    
    
    def delete_file(self,filename):
        self.session.delete(filename)
    
    def close_connection(self):
        self.session.quit()
