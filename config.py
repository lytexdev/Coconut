import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '!SuperSecretKey!')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = os.getenv('PORT', 8080)
    DEBUG = os.getenv('DEBUG', False)
    RATE_LIMIT = os.getenv('RATE_LIMIT', '300 per minute')
