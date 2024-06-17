import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = os.getenv('PORT', 8080)
    DEBUG = os.getenv('DEBUG', False)
    RATE_LIMIT = os.getenv('RATE_LIMIT', '5 per minute')
    
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    HASHED_PASSWORD = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    SHUTDOWN_COMMAND = os.getenv('SHUTDOWN_COMMAND', 'sudo shutdown -h now')
    REBOOT_COMMAND = os.getenv('REBOOT_COMMAND', 'sudo reboot')