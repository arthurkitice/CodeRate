from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Criteria(Base):
    __tablename__ = "criteria"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="criteria")

    evaluations = relationship(
        "Evaluation", 
        back_populates="criteria",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return f"Criteria(id={self.id}, name='{self.name}', description='{self.description}', user_id={self.user_id})"