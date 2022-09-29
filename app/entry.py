from os import path,environ
from io import BytesIO
from dotenv import load_dotenv
import requests,zipfile
import tarfile
from datetime import datetime
import ftplib


# Find .env file and load it
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'config.env'))

# Retrieve a file from a server
def get_file(url):
    req = requests.get(url)
    return req.content

# Unzip the file
def unzip_file(file):
    zip = zipfile.ZipFile(BytesIO(file))
    files= {}
    for file_details in zip.infolist():
        files[file_details.filename.split('/')[-1]] ={"content" : zip.open(file_details.filename).read(),"size": file_details.file_size,"date_time" : file_details.date_time} # content , size , datetime
    return files


# tar the file
def tar_files(files):
    tf = BytesIO()
    tf.filename= datetime.today().strftime('%Y%d%m') + '.tar.gz'
    with tarfile.open(fileobj=tf, mode='w:gz') as tar:
        for filename in files.keys():
            info = tarfile.TarInfo(filename)
            info.size = files[filename].get('size')
            tar.addfile(info, BytesIO(files[filename].get('content')))
    return tf

# store file in ftp
def  store_file(tar_file):
    session = ftplib.FTP('ftp','admin','admin')
    session.storbinary('STOR '+ tar_file.filename, BytesIO(tar_file.getvalue()))
    session.quit()



if __name__ == '__main__':
    url=environ.get('URL') + environ.get('FILE_NAME')
    print('Downloading file from: ' + url)
    file = get_file(url)
    files = unzip_file(file) # Returns a list of files
    tar_file = tar_files(files)
    store_file(tar_file)
  


    