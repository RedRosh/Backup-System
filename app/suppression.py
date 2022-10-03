from os import environ
from modules.DbHandler import DbHandler
from modules.ServerDistant import ServerDistant

db= DbHandler(environ.get('DB_HOST'),environ.get('DB_USER'),environ.get('DB_PASSWORD'),environ.get('DB_NAME'))
serverDistant = ServerDistant(environ.get('ftp_server_address'),environ.get('ftp_username'),environ.get('ftp_password'))
invalid_records = db.find_invalid_records()
for record in invalid_records:
    serverDistant.delete_file(record[2])
    db.delete_record(record[0])
serverDistant.close_connection()
db.close_connection()

