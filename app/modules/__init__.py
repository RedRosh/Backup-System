from os import path,environ
from dotenv import load_dotenv
from modules.ConfigHandler import ConfigHandler
import logging



basedir = path.abspath(path.dirname(__file__))
# Loading the .env file.
load_dotenv(path.join(basedir, '../.env'))
# setting up the logger
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=path.join(basedir, environ.get('LOG_FILE_PATH')), mode='w')
# Set the format that the logger needs to follow
formatter = logging.Formatter('{} %(asctime)s - %(levelname)s - %(message)s'.format(environ.get("LOGGER_NAME")))
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)
# loading config from yaml + validating the config.
ConfigHandler()


