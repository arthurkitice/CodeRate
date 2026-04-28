from pydantic import BaseModel
from models import Criteria
from dtos.evaluation_dto import EvaluationDTO

class CriteriaDTO(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    @classmethod
    def from_entity(cls, criteria: Criteria) -> "CriteriaWithEvaluationsDTO":
        return cls(
            id=criteria.id,
            name=criteria.name,
            description=criteria.description,
            user_id=criteria.user_id
        )

class CriteriaWithEvaluationsDTO(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    evaluations: list[EvaluationDTO]

    @classmethod
    def from_entity(cls, criteria: Criteria) -> "CriteriaWithEvaluationsDTO":
        return cls(
            id=criteria.id,
            name=criteria.name,
            description=criteria.description,
            user_id=criteria.user_id,
            evaluations=[EvaluationDTO.from_entity(e) for e in criteria.evaluations]
        )