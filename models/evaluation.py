from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    criteria_id = Column(Integer, ForeignKey("criteria.id", ondelete="CASCADE"))

    name = String

    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    submission_amount = Column(Integer)

    avg_score = Column(Float)

    criteria = relationship("Criteria", back_populates="evaluations")

    submissions = relationship(
        "Submission", 
        back_populates="evaluation", 
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def __repr__(self):
        return (
            f"Evaluation(id={self.id}, criteria_id={self.criteria_id}, name={self.name},"
            f"date='{self.date}', avg_score={self.avg_score}, submission_amount='{self.submission_amount}')"
        )