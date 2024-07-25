import json
from enum import Enum
from models import db

with open("./coconut-shell/src/modules.json") as f:
    modules_config = json.load(f)

ModuleEnum = Enum(
    "ModuleEnum",
    {module["enum"]: module["text"] for module in modules_config["modules"]},
)


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Enum(ModuleEnum), nullable=False)
    enabled = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Module {self.name}>"
