import ftplib
from io import BytesIO

class ServerDistant:
    
    session=None
    
    def __init__(self,server_address,username,password):
        self.session=ftplib.FTP(server_address,username,password)
    
    def add_file(self,file):   
        self.session.storbinary('STOR {}'.format(file.filename), BytesIO(file.getvalue()))
    
    
    
    
    def delete_file(self,filename):
        self.session.delete(filename)
    
    def close_connection(self):
        self.session.quit()
