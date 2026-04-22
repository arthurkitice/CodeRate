import os
from sqlalchemy.orm import Session
from repositories.submission_repository import SubmissionRepository
from models import Submission
from dtos.submission_dto import SubmissionDTO

class SubmissionService:
    def __init__(self):
        self.repository = SubmissionRepository()

    def create_submission(self, db: Session, evaluation_id: int, file_name: str, file_path: str, score: float, feedback: str) -> SubmissionDTO:
        # Validação de integridade: Garante que o ficheiro realmente existe no computador
        if not os.path.exists(file_path):
            raise ValueError(f"O ficheiro não foi encontrado no sistema: {file_path}")

        submission = Submission(
            evaluation_id=evaluation_id,
            file_name=file_name,
            file_path=file_path,
            score=score,
            feedback=feedback
        )

        self.repository.create(db, submission)

        return SubmissionDTO(
            id=submission.id,
            evaluation_id=submission.evaluation_id,
            file_name=submission.file_name,
            file_path=submission.file_path,
            date=submission.date,
            score=submission.score,
            feedback=submission.feedback
        )

    def get_submission_by_id(self, db: Session, submission_id: int) -> SubmissionDTO | None:
        submission = self.repository.get_by_id(db, submission_id)

        if not submission:
            return None
        
        return SubmissionDTO(
            id=submission.id,
            evaluation_id=submission.evaluation_id,
            file_name=submission.file_name,
            file_path=submission.file_path,
            date=submission.date,
            score=submission.score,
            feedback=submission.feedback
        )

    def list_submissions_by_evaluation(self, db: Session, evaluation_id: int) -> list[SubmissionDTO]:
        submissions = self.repository.list_by_evaluation_id(db, evaluation_id)
        return [
            SubmissionDTO(
                id=s.id,
                evaluation_id=s.evaluation_id,
                file_name=s.file_name,
                file_path=s.file_path,
                date=s.date,
                score=s.score,
                feedback=s.feedback
            ) for s in submissions
        ]

    def delete_submission(self, db: Session, submission_id: int) -> bool:
        submission = self.repository.get_by_id(db, submission_id)

        if not submission:
            return False
        
        return self.repository.delete(db, submission)