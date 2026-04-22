from sqlalchemy.orm import Session, joinedload
from models import Evaluation

class EvaluationRepository:
    def create(self, db: Session, evaluation: Evaluation) -> Evaluation:
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        return evaluation

    def get_by_id(self, db: Session, evaluation_id: int) -> Evaluation | None:
        return db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()

    def list_by_criteria_id(self, db: Session, criteria_id: int) -> list[Evaluation]:
        return db.query(Evaluation).filter(Evaluation.criteria_id == criteria_id).all()

    def get_evaluation_with_submissions(self, db: Session, evaluation_id: int) -> Evaluation | None:
        return db.query(Evaluation).options(joinedload(Evaluation.submissions)).filter(Evaluation.id == evaluation_id).first()

    def update(self, db: Session, evaluation: Evaluation) -> Evaluation:
        db.commit()
        db.refresh(evaluation)
        return evaluation

    def delete(self, db: Session, evaluation: Evaluation) -> bool:
        db.delete(evaluation)
        db.commit()
        return True