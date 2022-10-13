from os import environ,path
from modules.ConfigHandler import ConfigHandler
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant
from modules.FileManager import FileManager
from modules.ServerWeb import ServerWeb
from modules.EmailHandler import EmailHandler 
import logging

if __name__ == '__main__':
    try:
        validProcess = True   
        logger = logging.getLogger()
        config = ConfigHandler()
        logger.info("Script started.")
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
    except Exception as error:
        logger.error(str(error))
        validProcess = False
    finally:
        serverDistant.close_connection()
        logger.info("Server Distant Connection was closed successfully.")
        db.close_connection()
        logger.info("Database Connection was closed successfully.")
        logger.info("Script finished.")
        logger.info( config.get_notify() )
        if config.get_notify() == 1:
            logger.info("Sending email notification.")
            mail_server = EmailHandler(config.get_smtp_server() ,config.get_smtp_port(),config.get_smtp_mail_sender(),config.get_smtp_password())
            title = None
            body = None
            if validProcess:
               title= "Script Succeeded"
               body = "The script was executed successfully."
            else:
                title= "Script Failed"
                body = "The script failed to execute."
            mail_server.send_email(config.get_smtp_mail_receivers(),"Script Succeeded","Script finished")
            logger.info("Email was sent successfully.")


   
    
  


    
