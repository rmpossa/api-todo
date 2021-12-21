from app import db
from sqlalchemy.orm import relationship

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    tasks = relationship("Task", back_populates="user")
    
    def __eq__(self, other):
        if(isinstance(other, User)):
            return other.id == self.id

        return False

