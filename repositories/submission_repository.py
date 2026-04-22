from sqlalchemy.orm import Session
from models import Submission

class SubmissionRepository:
    def create(self, db: Session, submission: Submission) -> Submission:
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

    def get_by_id(self, db: Session, submission_id: int) -> Submission | None:
        return db.query(Submission).filter(Submission.id == submission_id).first()

    def list_by_evaluation_id(self, db: Session, evaluation_id: int) -> list[Submission]:
        return db.query(Submission).filter(Submission.evaluation_id == evaluation_id).all()

    def update(self, db: Session, submission: Submission) -> Submission:
        db.commit()
        db.refresh(submission)
        return submission

    def delete(self, db: Session, submission: Submission) -> bool:
        db.delete(submission)
        db.commit()
        return True