from dataclasses import dataclass
from datetime import datetime
from models import Submission

@dataclass
class SubmissionDTO:
    id: int
    evaluation_id: int
    file_name: str
    file_path: str
    content: str
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
            content=submission.content,
            date=submission.date,
            score=submission.score,
            feedback=submission.feedback
        )

@dataclass
class TempSubmissionDTO:
    file_name: str
    file_path: str
    content: str | None = None