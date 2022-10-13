from os import path
from dotenv import load_dotenv
from modules.ConfigHandler import ConfigHandler
'''
a small title 
'''


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))
ConfigHandler() 



