from sqlalchemy.orm import Session
from repositories.evaluation_repository import EvaluationRepository
from models import Evaluation
from dtos import EvaluationDTO, EvaluationWithSubmissionsDTO, SubmissionDTO

class EvaluationService:
    def __init__(self):
        self.repository = EvaluationRepository()

    def create_evaluation(self, db: Session, criteria_id: int, submission_amount: int = 0, avg_score: float = 0.0) -> EvaluationDTO:
        evaluation = Evaluation(
            criteria_id=criteria_id, 
            submission_amount=submission_amount, 
            avg_score=avg_score
        )
        self.repository.create(db, evaluation)
        
        return EvaluationDTO(
            id=evaluation.id,
            criteria_id=evaluation.criteria_id,
            date=evaluation.date,
            submission_amount=evaluation.submission_amount,
            avg_score=evaluation.avg_score
        )

    def get_evaluation_by_id(self, db: Session, evaluation_id: int) -> EvaluationDTO | None:
        evaluation = self.repository.get_by_id(db, evaluation_id)
        if not evaluation:
            return None
            
        return EvaluationDTO(
            id=evaluation.id,
            criteria_id=evaluation.criteria_id,
            date=evaluation.date,
            submission_amount=evaluation.submission_amount,
            avg_score=evaluation.avg_score
        )

    def list_evaluations_by_criteria(self, db: Session, criteria_id: int) -> list[EvaluationDTO]:
        evaluations = self.repository.list_by_criteria_id(db, criteria_id)
        return [
            EvaluationDTO(
                id=e.id,
                criteria_id=e.criteria_id,
                date=e.date,
                submission_amount=e.submission_amount,
                avg_score=e.avg_score
            ) for e in evaluations
        ]

    def get_evaluation_with_submissions(self, db: Session, evaluation_id: int) -> EvaluationWithSubmissionsDTO | None:
        evaluation = self.repository.get_evaluation_with_submissions(db, evaluation_id)
        if not evaluation:
            return None
        
        # Converte as submissões filhas para DTO
        submissions_dto = [
            SubmissionDTO(
                id=s.id,
                evaluation_id=s.evaluation_id,
                file_name=s.file_name,
                file_path=s.file_path,
                date=s.date,
                score=s.score,
                feedback=s.feedback
            ) for s in evaluation.submissions
        ]

        return EvaluationWithSubmissionsDTO(
            id=evaluation.id,
            criteria_id=evaluation.criteria_id,
            date=evaluation.date,
            submission_amount=evaluation.submission_amount,
            avg_score=evaluation.avg_score,
            submissions=submissions_dto
        )

    def update_evaluation(self, db: Session, evaluation_id: int, submission_amount: int = None, avg_score: float = None) -> EvaluationDTO | None:
        evaluation = self.repository.get_by_id(db, evaluation_id)
        if not evaluation:
            return None
        
        if submission_amount is not None:
            evaluation.submission_amount = submission_amount
        if avg_score is not None:
            evaluation.avg_score = avg_score
            
        updated = self.repository.update(db, evaluation)
        return EvaluationDTO(
            id=updated.id,
            criteria_id=updated.criteria_id,
            date=updated.date,
            submission_amount=updated.submission_amount,
            avg_score=updated.avg_score
        )

    def delete_evaluation(self, db: Session, evaluation_id: int) -> bool:
        evaluation = self.repository.get_by_id(db, evaluation_id)
        if not evaluation:
            return False
        return self.repository.delete(db, evaluation)