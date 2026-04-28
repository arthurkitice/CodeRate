from pydantic import BaseModel
from datetime import datetime
from models import Submission

class SubmissionDTO(BaseModel):
    id: int
    evaluation_id: int
    file_name: str
    file_path: str
    date: datetime
    score: float
    feedback: str

    @classmethod
    def from_entity(cls, submission: Submission) -> "SubmissionDTO":
        return cls(
            id=submission.id,
            evaluation_id=submission.evaluation_id,
            file_name=submission.file_name,
            file_path=submission.file_path,
            date=submission.date,
            score=submission.score,
            feedback=submission.feedback
        )
    