import psycopg2


class DbHandler:
    ''' ##**Cette classe nous permet de manipuler la base de données qui reflète ce qui se passe au niveau du serveur distant.** '''
    connection = None
    '''C'est la variable qui nous permet d'intéragir avec notre base de données.'''
    
    def __init__(self, host, user, password, database):
        self.connection =  psycopg2.connect( host=host,database=database,user=user,password=password)

    def find_invalid_records(self):
        '''Récupération d'un tuple qui contient les fichiers invalides.'''
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {} OR is_valid={};".format(True,False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 

    def update_all(self,checksum=""):
        '''La mise à jour de la validité des fichiers contenus dans la base de données en fonction du *Hash*.'''
        sql = "UPDATE archivage_files SET is_valid= {} WHERE checksum != '{}';".format(False,checksum)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()

    def find_all(self):
        '''Sélection des fichiers qui n'ont pas encore dépassé le délai d'expiration sous forme d'un tuple.'''
        sql = "SELECT * FROM v_archivage_files WHERE is_expired = {};".format(False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
        
        
    def add_record(self,checksum,expiration_date,filename):
        '''Ajout des fichiers qui sont caractérisés par : 
        
        - **Nom du fichier**
        - **Hash**
        - **délai d'expiration**'''
        sql = """INSERT INTO archivage_files(checksum,expiration_date,filename) VALUES(%s,%s,%s)"""
        cur = self.connection.cursor()
        cur.execute(sql, (checksum,expiration_date ,filename))
        self.connection.commit()
        cur.close()
    
    def delete_record(self,file_id):
        '''Suppression des fichiers.'''
        sql = "DELETE FROM archivage_files WHERE file_id = {}".format(file_id)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()
         
        
    def update_record(self,checksum,is_valid,expiration_date):
        '''La mise à jour de la validité et le délai d'expiration des fichiers.'''
        sql = "UPDATE archivage_files SET expiration_date = '{}', is_valid= {} WHERE checksum = '{}';".format(expiration_date,is_valid,checksum)
        cur = self.connection.cursor()
        cur.execute(sql)
        self.connection.commit()
        cur.close()

    
    def find_record(self,checksum):
        '''Récupération des fichiers non expirés.'''
        sql = "SELECT * FROM v_archivage_files WHERE checksum = '{}' AND is_expired = {};".format(checksum,False)
        cur = self.connection.cursor()
        cur.execute(sql)
        records= cur.fetchall()
        cur.close()
        return records 
            
    def close_connection(self):
        '''Déconnexion.'''
        self.connection.close()


    