import configparser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
config_file = 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)

JWT_SECRET = config.get('DEFAULT','JWT_SECRET')
EXPIRY = config.getint('DEFAULT','EXPIRY')

DB_USER = config["DATABASE"]["user"]
DB_PASSWORD = config["DATABASE"]["password"]
DB_HOST = config["DATABASE"]["host"]
DB_PORT = config["DATABASE"]["port"]
DB_NAME = config["DATABASE"]["name"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  
def load_admin_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "admin" not in config:
        raise ValueError("Missing [admin] section in config.ini")

    return {
        "username": config["admin"]["username"],
        "email": config["admin"]["email"],
        "password": config["admin"]["password"],
    }