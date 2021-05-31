from app import db


class Task (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    def __eq__(self, other):
        if(isinstance(other, Task)):
            return other.id == self.id

        return False


