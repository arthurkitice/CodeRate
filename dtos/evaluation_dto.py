# dtos/evaluation_dto.py
from dataclasses import dataclass
from datetime import datetime
from dtos.submission_dto import SubmissionDTO 

@dataclass
class EvaluationDTO:
    id: int
    criteria_id: int
    date: datetime
    submission_amount: int
    avg_score: float

@dataclass
class EvaluationWithSubmissionsDTO:
    id: int
    criteria_id: int
    date: datetime
    submission_amount: int
    avg_score: float
    submissions: list[SubmissionDTO]