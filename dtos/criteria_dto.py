from dataclasses import dataclass
from dtos.evaluation_dto import EvaluationDTO

@dataclass
class CriteriaDTO:
    id: int
    name: str
    description: str
    user_id: int

@dataclass
class CriteriaWithEvaluationsDTO:
    id: int
    name: str
    description: str
    user_id: int
    evaluations: list[EvaluationDTO]