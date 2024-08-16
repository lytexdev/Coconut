from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .setup import Setup
from .user import User
from .module import Module
from .backup import Backup