from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def update(self, db: Session, new_user: User) -> User | None:
        db.commit()
        db.refresh(new_user)
        return new_user

    def delete(self, db: Session, user: User) -> bool:
        db.delete(user)
        db.commit()
        return True