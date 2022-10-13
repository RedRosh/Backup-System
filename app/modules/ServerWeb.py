import requests
import logging


logger = logging.getLogger()
class ServerWeb :
    ''' ##**La classe qui gère le serveur web**.'''
    base_url = ''
    '''L'url de notre serveur web.'''
    
    def __init__(self, base_url):
        self.base_url = base_url
        
    def retrieve_file(self,filename):
        '''Récupération du fichier à partir du serveur.'''
        # We are using the requests library to retrieve the file from the server.
        response = requests.get('{}{}'.format(self.base_url,filename))
        # we got different cases that we need to handle based on the response status code.
        match response.status_code:
            case 200:
                # All good, we just to return the file.
                logger.info("File retrieved successfully.")
                return response.content
            case 404:
                # The file doesn't exist.
                raise Exception("File not found.")
            case _:
                # Any other case.
                raise Exception("An error occurred while retrieving the file.")
        
      
    
