from os import path,environ
from cerberus import Validator
import yaml


schema = {'VERSIONING': {'type': 'integer','min':0,'max':1},
        'EXPIRED_IN' : {'type': 'integer','min':0},
        'SMTP_PORT':{'type': 'integer','min':0},
        'SMTP_SERVER':{'type': 'string','minlength': 8},
        'SMTP_MAIL_SENDER':{
            "type": "string",
            "minlength": 8,
            "maxlength": 255,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        'SMTP_PASSWORD':{'type': 'string','minlength': 8},
        'SMTP_MAIL_RECEIVERS' :{ 'type': 'list', 'schema': {'type': 'string', "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"}} ,
        'NOTIFY':{'type': 'integer','min':0,'max':1},
        'ADD_ATTACHMENT':{'type': 'integer','min':0,'max':1},
    }

v = Validator(schema)


class ConfigHandler:
    ''' ##**Cette classe nous permet de manipuler la configuration en se basant sur les critères suivant :**

        - ***Historisation*** : si elle est activée ou pas.
        - ***Délai d'expiration*** : présenté par le nombre des jours. '''
    config = None
    '''À priori, cette variable présente le dictionnaire qui constitue notre configuration. '''
    
    def __init__(self):
        ''' this is the main '''
        if ConfigHandler.config != None:
            return
    
        basedir = path.abspath(path.dirname(__file__))
        with open(path.join(basedir,environ.get('CONFIG_PATH')), "r") as yamlfile:
            ConfigHandler.config = yaml.load(yamlfile, Loader=yaml.FullLoader)
            valid= v.validate(self.config,schema)
            errors = v.errors
            print(errors)
            yamlfile.close()
            if not valid:
                print('Not valid',errors,valid)
                exit(1)
                
    def get_versioning(self):
        '''C'est le *getter* qui nous permet de récupèrer la valeur de *l'Historisation*.'''
        return ConfigHandler.config['VERSIONING']
    
    
    def get_expired_in(self):
        '''C'est le *getter* qui nous permet de récupèrer la valeur du *délai d'expiration*.'''
        return ConfigHandler.config['EXPIRED_IN']
    
    def get_smtp_port(self):
        return ConfigHandler.config['SMTP_PORT']

    def get_smtp_server(self):
        return ConfigHandler.config['SMTP_SERVER']
    
    def get_smtp_mail_sender(self):
        return ConfigHandler.config['SMTP_MAIL_SENDER']
    
    def get_smtp_password(self):
        return ConfigHandler.config['SMTP_PASSWORD']

    def get_smtp_mail_receivers(self):
        return ConfigHandler.config['SMTP_MAIL_RECEIVERS']
    
    def get_notify(self):
        return ConfigHandler.config['NOTIFY']
    
    def get_add_attachment(self):
        return ConfigHandler.config['ADD_ATTACHMENT']
