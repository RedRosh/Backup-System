import psycopg2


class DbHandler:
    connection = None
    
    def __init__(self, host, user, password, database):
        self.connection =  psycopg2.connect( host=host,database=database,user=user,password=password)

    def find_invalid_records(self):
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {} OR is_valid={};".format(True,False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 

    def update_all(self,checksum=""):
        sql = "UPDATE archivage_files SET is_valid= {} WHERE checksum != '{}';".format(False,checksum)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()

    def find_all(self):
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {};".format(False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
        
        
    def add_record(self,checksum,expiration_date,filename):
        sql = """INSERT INTO archivage_files(checksum,expiration_date,filename) VALUES(%s,%s,%s)"""
        cur = self.connection.cursor()
        cur.execute(sql, (checksum,expiration_date ,filename))
        self.connection.commit()
        cur.close()
    
    def delete_record(self,file_id):
        sql = "DELETE FROM archivage_files WHERE file_id = {}".format(file_id)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()
         
        
    def update_record(self,checksum,is_valid,expiration_date):
        sql = "UPDATE archivage_files SET expiration_date = '{}', is_valid= {} WHERE checksum = '{}';".format(expiration_date,is_valid,checksum)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()

    
    def find_record(self,checksum):
        sql = "SELECT * FROM v_archivage_files WHERE checksum = '{}' AND is_expired = {};".format(checksum,False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
            
    def close_connection(self):
        self.connection.close()


    