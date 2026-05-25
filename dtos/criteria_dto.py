from pydantic import BaseModel
from models import Criteria
from dtos.evaluation_dto import EvaluationDTO

class CriteriaDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, criteria: Criteria) -> "CriteriaWithEvaluationsDTO":
        return cls(
            id=criteria.id,
            name=criteria.name,
            description=criteria.description
        )

class CriteriaWithEvaluationsDTO(BaseModel):
    id: int
    name: str
    description: str
    
    evaluations: list[EvaluationDTO]

    @classmethod
    def from_entity(cls, criteria: Criteria) -> "CriteriaWithEvaluationsDTO":
        return cls(
            id=criteria.id,
            name=criteria.name,
            description=criteria.description,
            evaluations=[EvaluationDTO.from_entity(e) for e in criteria.evaluations]
        )