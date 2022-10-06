import requests

class ServerWeb :
    ''' ##**La classe qui gère le serveur web**.'''
    base_url = ''
    '''L'url de notre serveur web.'''
    
    def __init__(self, base_url):
        self.base_url = base_url
        
    def retrieve_file(self,filename):
        '''Récupération du fichier à partir du serveur.'''
        response = requests.get('{}{}'.format(self.base_url,filename))
        return response.content