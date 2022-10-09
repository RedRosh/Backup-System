import requests
import logging


logger = logging.getLogger()
class ServerWeb :
    base_url = ''
    
    def __init__(self, base_url):
        self.base_url = base_url
        
    def retrieve_file(self,filename):
        response = requests.get('{}{}'.format(self.base_url,filename))
        match response.status_code:
            case 200:
                logger.info("File retrieved successfully.")
                return response.content
            case 404:
                raise Exception("File not found.")
            case _:
                raise Exception("An error occurred while retrieving the file.")
        
      
    
