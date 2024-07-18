import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = os.getenv('PORT', 8080)
    DEBUG = os.getenv('DEBUG', False)
    RATE_LIMIT = os.getenv('RATE_LIMIT', '60 per minute')
