from models import db


class Backup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    backup_path = db.Column(db.String(255), nullable=False)
    destination_path = db.Column(db.String(255), nullable=False)
    excluded_paths = db.Column(db.String(255), nullable=True)
    scheduled_time = db.Column(db.String(255), nullable=True) # cron format
    max_backups = db.Column(db.Integer, nullable=True, default=5)
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Backup {self.name}>"