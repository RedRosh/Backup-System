import psycopg2


class DbHandler:
    connection = None
    
    def __init__(self, host, user, password, database):
        self.connection =  psycopg2.connect( host=host,database=database,user=user,password=password)
     
            
    def close_connection(self):
        self.connection.close()


    