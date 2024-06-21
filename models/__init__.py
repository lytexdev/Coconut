from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.setup import Setup
from models.user import User
from models.module import Module
