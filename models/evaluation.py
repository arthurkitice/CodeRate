from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    criteria_id = Column(Integer, ForeignKey("criteria.id"))

    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    submission_amount = Column(Integer)

    avg_score = Column(Float)

    evaluation = relationship("Submission", back_populates="evaluation")

    def __repr__(self):
        return (
            f"Evaluation(id={self.id}, criteria_id={self.criteria_id}, "
            f"date='{self.date}', avg_score={self.avg_score}, submission_ammount='{self.submission_amount}')"
        )