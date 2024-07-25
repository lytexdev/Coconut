import uuid
from enum import Enum
from models import db
from sqlalchemy.dialects.postgresql import UUID


class RoleEnum(Enum):
    ADMIN = "Admin"


class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
