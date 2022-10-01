import requests

class ServerWeb :
    base_url = ''
    
    def __init__(self, base_url):
        self.base_url = base_url
        
    def retrieve_file(self,filename):
        response = requests.get('{}{}'.format(self.base_url,filename))
        return response.content