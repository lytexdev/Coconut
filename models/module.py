from enum import Enum
from models import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ModuleEnum(Enum):
    SYSTEM = "System"
    BACKUP = "Backup"
    DOCKER = "Docker"


class Module(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Enum(ModuleEnum), nullable=False)
    enabled = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Module {self.name}>"
