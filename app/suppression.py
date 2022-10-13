from os import environ
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant


if __name__ == '__main__':
    '''
    The main goal of this script is to clean the database && distant server from the expired files.
    the script will be executed every day at 12:00 PM, by doing so we will assure that our distant server will be clean of any expired files without checking or deleting them manually.
    '''
    # Init the db && distant server
    db= DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
    serverDistant = ServerDistant(environ.get('ftp_server_address'),environ.get('ftp_username'),environ.get('ftp_password'))
    # Selecting all invalid records from the db.
    invalid_records = db.find_invalid_records()
    for record in invalid_records:
        serverDistant.delete_file(record[2]) # Deleting the file from the distant server.
        db.delete_record(record[0]) # Deleting the file from the db.
    # Closing connections to avoid any security / memory issues.
    serverDistant.close_connection()
    db.close_connection()

