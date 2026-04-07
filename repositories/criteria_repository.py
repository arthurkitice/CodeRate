from sqlalchemy.orm import Session
from models import Criteria

class CriteriaRepository:
    def create(self, db: Session, criteria: Criteria) -> Criteria:
        db.add(criteria)
        db.commit()
        db.refresh(criteria)
        return criteria

    def get_all(self, db: Session) -> list[Criteria]:
        return db.query(Criteria).all()

    def get_by_id(self, db: Session, criteria_id: int) -> Criteria | None:
        return db.query(Criteria).filter(Criteria.id == criteria_id).first()
    
    def list_by_user_id(self, db: Session, user_id: int) -> list[Criteria]:
        return db.query(Criteria).filter(Criteria.user_id == user_id).all()

    def update(self, db: Session, criteria: Criteria) -> Criteria | None:
        db.commit()
        db.refresh(criteria)
        return criteria

    def delete(self, db: Session, criteria: Criteria) -> bool:
        db.delete(criteria)
        db.commit()
        return True