from dataclasses import dataclass
from datetime import datetime

@dataclass
class SubmissionDTO:
    id: int
    evaluation_id: int
    file_name: str
    file_path: str
    date: datetime
    score: float
    feedback: str