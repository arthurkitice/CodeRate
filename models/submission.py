from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id"))
    
    file_name = Column(String)
    file_path = Column(String)
    
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    score = Column(Float)
    feedback = Column(Text)

    evaluation = relationship("Evaluation", back_populates="submission")

    def __repr__(self):
        return (
            f"Submission(id={self.id}, evaluation_id={self.evaluation_id}, "
            f"file_name='{self.file_name}', file_path='{self.file_path}', "
            f"date='{self.date}', score={self.score}, feedback='{self.feedback}')"
        )