import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Set Flask configuration variables from .env file
    """
    SECRET_KEY = os.getenv('SECRET_KEY', '!SuperSecretKey!')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = os.getenv('PORT', 8080)
    DEBUG = os.getenv('DEBUG', False)
    RATE_LIMIT = os.getenv('RATE_LIMIT', '240 per minute')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*')
    WHITELIST = os.getenv('WHITELIST', False)
    IP_WHITELIST = os.getenv('IP_WHITELIST', '127.0.0.1,192.168.0.1')
    IP_BLACKLIST = os.getenv('IP_BLACKLIST', '')
