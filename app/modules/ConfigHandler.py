from os import path,environ
from cerberus import Validator
import yaml

schema = {'VERSIONING': {'type': 'integer','min':0,'max':1},
        'EXPIRED_IN' : {'type': 'integer','min':0},
        }
v = Validator(schema)


class ConfigHandler:
    data = None
    
    def __init__(self):
        ''' this is the main '''
        if ConfigHandler.data != None:
            return
    
        basedir = path.abspath(path.dirname(__file__))
        with open(path.join(basedir,environ.get('CONFIG_PATH')), "r") as yamlfile:
            self.data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            valid= v.validate(self.data,schema)
            errors = v.errors
            yamlfile.close()
            if not valid:
                print('Not valid',errors,valid)
                exit(1)
                
    def get_versioning(self):
        return self.data['VERSIONING']
    
    def get_expired_in(self):
        return self.data['EXPIRED_IN']
        