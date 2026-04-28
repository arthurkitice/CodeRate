from pydantic import BaseModel
from datetime import datetime
from dtos.submission_dto import SubmissionDTO 
from models import Evaluation

class EvaluationDTO(BaseModel):
    id: int
    criteria_id: int
    name: str
    date: datetime
    submission_amount: int
    avg_score: float

    @classmethod
    def from_entity(cls, evaluation: Evaluation) -> "EvaluationDTO":
        return cls(
            id=evaluation.id,
            criteria_id=evaluation.criteria_id,
            name=evaluation.name,
            date=evaluation.date
        )

class EvaluationWithSubmissionsDTO(BaseModel):
    id: int
    criteria_id: int
    name: str
    date: datetime
    submission_amount: int
    avg_score: float
    submissions: list[SubmissionDTO]

    @classmethod
    def from_entity(cls, evaluation: Evaluation) -> "EvaluationWithSubmissionsDTO":
        return cls(
            id=evaluation.id,
            criteria_id=evaluation.criteria_id,
            name=evaluation.name,
            date=evaluation.date,
            submissions=[EvaluationDTO.from_entity(s) for s in evaluation.submissions]
        )