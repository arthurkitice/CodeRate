from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Similarity(Base):
    __tablename__ = "similarities"

    id = Column(Integer, primary_key=True)
    
    # O arquivo que está sendo alertado
    source_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"))
    
    # O arquivo com o qual ele se parece
    target_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"))
    
    # A porcentagem de semelhança (Ex: 0.85 para 85%)
    match_ratio = Column(Float)

    # Relacionamentos bidirecionais
    source_submission = relationship("Submission", foreign_keys=[source_id], backref="similarities_found")
    target_submission = relationship("Submission", foreign_keys=[target_id])