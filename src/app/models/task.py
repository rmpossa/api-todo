from sqlalchemy.sql.schema import ForeignKey
from app import db
from sqlalchemy.orm import relationship

class Task (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="tasks")

    def __eq__(self, other):
        if(isinstance(other, Task)):
            return other.id == self.id

        return False


