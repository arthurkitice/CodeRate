from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    criteria = relationship("Criteria", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}')"

class Criteria(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="criteria")

    def __repr__(self):
        return f"Criteria(id={self.id}, name='{self.name}', description='{self.description}', user_id={self.user_id})"