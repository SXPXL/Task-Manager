import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
config_file = 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)

DATABASE_URL = config.get('DEFAULT','DATABASE_URL')
JWT_SECRET = config.get('DEFAULT','JWT_SECRET')
EXPIRY = config.getint('DEFAULT','EXPIRY')
  