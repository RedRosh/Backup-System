from os import path,environ
from dotenv import load_dotenv
from modules.ConfigHandler import ConfigHandler
import logging


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))
ConfigHandler()
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=path.join(basedir, environ.get('LOG_FILE_PATH')), mode='a')
formatter = logging.Formatter('{} %(asctime)s - %(levelname)s - %(message)s'.format(environ.get("LOGGER_NAME")))
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)



