import psycopg2


class DbHandler:
    connection = None
    
    def __init__(self, host, user, password, database):
        self.connection =  psycopg2.connect( host=host,database=database,user=user,password=password)
     
    
    def add_record(self,checksum,expiration_date,filename):
        sql = """INSERT INTO archivage_files(checksum,expiration_date,filename) VALUES(%s,%s,%s)"""
        cur = self.connection.cursor()
        cur.execute(sql, (checksum,expiration_date ,filename))
        cur.close()
            
    def close_connection(self):
        self.connection.close()


    