import zipfile
from io import BytesIO
from datetime import datetime
import tarfile
import hashlib
import logging

logger = logging.getLogger()
class FileManager:
    ''' ##**La classe qui nous permet de manipuler les fichiers récupérés.**'''
    
    
    @staticmethod
    def rename(file,name):
        '''Pour renommer le fichier récupéré.'''
        # renaming the file.
        file.filename = name
        return file
    
    @staticmethod
    def get_hash(file):
        '''Récupération du hash.'''
        logger.info("Successfully calculating hash of file.")
        # Calculating the hash of the file using Sha256 algorithm. ( using Sha256 because it's the most secure algorithm )
        return hashlib.sha256( BytesIO(file).read()).hexdigest()
        
    
    
    @staticmethod
    def unzip_file(file):
        '''La fonction pour dézipper.'''
        # loading the zip file 
        zip = zipfile.ZipFile(BytesIO(file))
        
        files= {}
        # Iterating over the files in the zip file.
        for file_details in zip.infolist():
            # Checking if the zip contains .sql inside it.
            if '.sql' not in file_details.filename:
                raise Exception("File {} is not a sql file.".format(file_details.filename))
            # Extracting the file from the zip file + adding it to the files dictionary.
            files[file_details.filename.split('/')[-1]] ={"content" : zip.open(file_details.filename).read(),"size": file_details.file_size,"date_time" : file_details.date_time} # content , size , datetime
        logger.info("Successfully unzipped file.")
        # return a dictionary containing the files content + meta-data.
        return files
    
    @staticmethod
    def tar_files(files):
        '''Pour changer en format tar.'''
        # Creating an empty Byte Array
        tf = BytesIO()
        # Setting the filename 
        tf.filename= datetime.today().strftime('%Y%d%m') + '.tar.gz'
        with tarfile.open(fileobj=tf, mode='w:gz') as tar:
            # Iterating over the files dictionary.
            for filename in files.keys():
                info = tarfile.TarInfo(filename)
                info.size = files[filename].get('size')
                # Add file to the tar
                tar.addfile(info, BytesIO(files[filename].get('content')))
        logger.info("Successfully tarred file with name {}.".format(tf.filename))
        # returning the tar file.
        return tf
        