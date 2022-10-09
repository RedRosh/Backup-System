import zipfile
from io import BytesIO
from datetime import datetime
import tarfile
import hashlib
import logging

logger = logging.getLogger()
class FileManager:
    
    
    @staticmethod
    def rename(file,name):
        file.filename = name
        return file
    
    
    @staticmethod
    def get_hash(file):
        logger.info("Successfully calculating hash of file.")
        return hashlib.sha256( BytesIO(file).read()).hexdigest()
        
    
    @staticmethod
    def unzip_file(file):
        zip = zipfile.ZipFile(BytesIO(file))
        
        files= {}
        for file_details in zip.infolist():
            if '.sql' not in file_details.filename:
                raise Exception("File {} is not a sql file.".format(file_details.filename))
            files[file_details.filename.split('/')[-1]] ={"content" : zip.open(file_details.filename).read(),"size": file_details.file_size,"date_time" : file_details.date_time} # content , size , datetime
        logger.info("Successfully unzipped file.")
        return files
    
    @staticmethod
    def tar_files(files):
        tf = BytesIO()
        tf.filename= datetime.today().strftime('%Y%d%m%H%M%S') + '.tar.gz'
        with tarfile.open(fileobj=tf, mode='w:gz') as tar:
            for filename in files.keys():
                info = tarfile.TarInfo(filename)
                info.size = files[filename].get('size')
                tar.addfile(info, BytesIO(files[filename].get('content')))
        logger.info("Successfully tarred file with name {}.".format(tf.filename))
        return tf
        