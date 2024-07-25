import uuid
from enum import Enum
from models import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property


class RoleEnum(Enum):
    ADMIN = "Admin"


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext) if plaintext else None

    def check_password_hash(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def __repr__(self):
        return f"<User {self.username}>"