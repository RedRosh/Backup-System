from os import environ
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant
from modules.FileManager import FileManager
from modules.ServerWeb import ServerWeb

db= DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
serverWeb = ServerWeb(environ.get('URL'))
serverDistant = ServerDistant(environ.get('ftp_server_address'),environ.get('ftp_username'),environ.get('ftp_password'))
file = serverWeb.retrieve_file(environ.get('FILE_NAME')) 
hash = FileManager.get_hash(file)
files = FileManager.unzip_file(file)
tar_file = FileManager.tar_files(files)
serverDistant.add_file(tar_file,hash)   
invalid_records = db.find_invalid_records()
for record in invalid_records:
    serverDistant.delete_file(record[2])
    db.delete_record(record[0])

serverDistant.close_connection()
db.close_connection()
   
    
  


    
