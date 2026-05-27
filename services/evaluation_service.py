from repositories.evaluation_repository import EvaluationRepository
from models import Evaluation
from dtos import EvaluationDTO, EvaluationWithSubmissionsDTO, SubmissionDTO
from database import get_db

class EvaluationService:
    def __init__(self):
        self.repository = EvaluationRepository()

    def create_evaluation(self, criteria_id: int, name: str) -> EvaluationDTO:
        evaluation = Evaluation(
            criteria_id=criteria_id, 
            name=name
        )
        with get_db() as db:
            self.repository.create(db, evaluation)
            return EvaluationDTO.from_entity(evaluation)

    def get_evaluation_by_id(self, evaluation_id: int) -> EvaluationDTO | None:
        with get_db() as db:
            evaluation = self.repository.get_by_id(db, evaluation_id)
            if not evaluation:
                return None
            return EvaluationDTO.from_entity(evaluation)

    def list_evaluations_by_criteria(self, criteria_id: int) -> list[EvaluationDTO]:
        with get_db() as db:
            evaluations = self.repository.list_by_criteria_id(db, criteria_id)
            return [EvaluationDTO.from_entity(e) for e in evaluations]

    def get_evaluation_with_submissions(self, evaluation_id: int) -> EvaluationWithSubmissionsDTO | None:
        with get_db() as db:
            evaluation = self.repository.get_evaluation_with_submissions(db, evaluation_id)
            if not evaluation:
                return None
            return EvaluationWithSubmissionsDTO.from_entity(evaluation)

    def update_evaluation(self, evaluation_id: int, name: str = None) -> EvaluationDTO | None:
        with get_db() as db:
            evaluation = self.repository.get_by_id(db, evaluation_id)
            if not evaluation:
                return None
            
            if name is not None:
                evaluation.name = name
                
            updated = self.repository.update(db, evaluation)
            return EvaluationDTO.from_entity(updated)

    def delete_evaluation(self, evaluation_id: int) -> bool:
        with get_db() as db:
            evaluation = self.repository.get_by_id(db, evaluation_id)
            if not evaluation:
                return False
            return self.repository.delete(db, evaluation)