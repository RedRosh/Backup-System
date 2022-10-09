import psycopg2
import logging


logger = logging.getLogger()
class DbHandler:
    connection = None
    
    def __init__(self, host, user, password, database):
        if(DbHandler.connection != None):
            return
        DbHandler.connection = psycopg2.connect(host=host, user=user, password=password, database=database)
        logger.info("Connection to database was established.")

        
            
    def find_invalid_records(self):
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {} OR is_valid={};".format(True,False)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 

    def update_all(self,checksum=""):
        sql = "UPDATE archivage_files SET is_valid= {} WHERE checksum != '{}';".format(False,checksum)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        DbHandler.connection.commit()
        cur.close()

    def find_all(self):
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {};".format(False)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
        
        
    def add_record(self,checksum,expiration_date,filename):
        sql = """INSERT INTO archivage_files(checksum,expiration_date,filename) VALUES(%s,%s,%s)"""
        cur = DbHandler.connection.cursor()
        cur.execute(sql, (checksum,expiration_date ,filename))
        DbHandler.connection.commit()
        cur.close()
    
    def delete_record(self,file_id):
        sql = "DELETE FROM archivage_files WHERE file_id = {}".format(file_id)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        DbHandler.connection.commit()
        cur.close()
         
        
    def update_record(self,checksum,is_valid,expiration_date):
        sql = "UPDATE archivage_files SET expiration_date = '{}', is_valid= {} WHERE checksum = '{}';".format(expiration_date,is_valid,checksum)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        DbHandler.connection.commit()
        cur.close()

    
    def find_record(self,checksum):
        sql = "SELECT * FROM v_archivage_files WHERE checksum = '{}' AND is_expired = {};".format(checksum,False)
        cur = DbHandler.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
            
    def close_connection(self):
        DbHandler.connection.close()


    