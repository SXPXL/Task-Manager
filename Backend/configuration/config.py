"""
Configuration Loader
-------------------
Loads application configuration from config.ini and provides constants for use throughout the backend.

Features:
- Reads JWT secret and expiry from the DEFAULT section
- Reads database connection parameters from the DATABASE section
- Constructs the DATABASE_URL for SQLAlchemy
- Provides a function to load admin credentials from the config file

Constants:
- JWT_SECRET: Secret key for JWT token encoding
- EXPIRY: Token expiry time (in minutes)
- DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME: Database connection parameters
- DATABASE_URL: Full SQLAlchemy database URL

Functions:
- load_admin_config: Loads admin credentials (username, email, password) from the [admin] section
"""

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
    """
    Loads admin credentials from the [admin] section of config.ini.
    
    Returns:
        dict: Dictionary with keys 'username', 'email', and 'password'.
    Raises:
        ValueError: If the [admin] section is missing in config.ini.
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "admin" not in config:
        raise ValueError("Missing [admin] section in config.ini")

    return {
        "username": config["admin"]["username"],
        "email": config["admin"]["email"],
        "password": config["admin"]["password"],
    }