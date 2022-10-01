from os import environ
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant
from modules.FileManager import FileManager
from modules.ServerWeb import ServerWeb

        

if __name__ == '__main__':
    serverWeb = ServerWeb(environ.get('URL'))
    db =  DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
    serverDistant = ServerDistant(environ.get('ftp_server_address'),environ.get('ftp_username'),environ.get('ftp_password'))
    file = serverWeb.retrieve_file(environ.get('FILE_NAME')) 
    files = FileManager.unzip_file(file) # Returns a list of files
    tar_file = FileManager.tar_files(files)
    serverDistant.add_file(tar_file)     
    db.close_connection()   
    serverDistant.close_connection()
   
    
  


    
