from models import db


class Setup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Setup {self.completed}>"
