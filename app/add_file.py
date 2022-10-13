from os import environ
from modules.ConfigHandler import ConfigHandler
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant
from modules.FileManager import FileManager
from modules.ServerWeb import ServerWeb
from modules.EmailHandler import EmailHandler

import logging

if __name__ == '__main__':
    try:
        validProcess = True   # This variable determines if the process has succeeded or not.
        # Init logger && config Handler.
        logger = logging.getLogger()
        config = ConfigHandler()
        logger.info("Script started.")
        # Init the db && distant server  && server web.
        db= DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
        serverWeb = ServerWeb(environ.get('URL'))
        serverDistant = ServerDistant(environ.get('ftp_server_address'),environ.get('ftp_username'),environ.get('ftp_password'))
        # Getting the file from the server web.
        file = serverWeb.retrieve_file(environ.get('FILE_NAME'))
        # Hashing the file in order to check the integrity of the file after uploading it to the distant server.
        hash = FileManager.get_hash(file)
        # Applying modification to the retrieved file such as : unzip + compress
        files = FileManager.unzip_file(file)
        tar_file = FileManager.tar_files(files)
        # Uploading the file to the distant server while taking in consideration the versioning && expired in  props in the config file
        serverDistant.add_file(tar_file,hash)
        # Cleaning the distant server / Data base  from the expired files.
        invalid_records = db.find_invalid_records() # Getting the expired files from the db && distant server.
        for record in invalid_records:
            serverDistant.delete_file(record[2]) # Deleting the file from the distant server.
            db.delete_record(record[0])  # Deleting the file from the db.
    except Exception as error:
        # Logging the errors.
        logger.error(str(error))
        validProcess = False
    finally:
        # Closing connections to avoid any security / memory issues.
        serverDistant.close_connection()
        logger.info("Server Distant Connection was closed successfully.")
        db.close_connection()
        logger.info("Database Connection was closed successfully.")
        logger.info("Script finished.")
        # Send Email to the admin based on notify props in the config file.
        if config.get_notify() == 1:
            # Sending Email with the resume of all the events && the log file. 
            mail_server = EmailHandler(config.get_smtp_server() ,config.get_smtp_port(),config.get_smtp_mail_sender(),config.get_smtp_password()) 
            # Send different template based on the status of the process.
            if validProcess:
                # case of success
                mail_server.send_email(config.get_smtp_mail_receivers(),"Script Succeeded","Script finished")
            else:
                # case of failure
                mail_server.send_email(config.get_smtp_mail_receivers(),"Process Failed","Script finished")
     

   
    
  


    
