from sqlalchemy.orm import Session
from models import User

class UserRepository:
    def create(self, db: Session, name: str, email: str, password: str) -> User:
        user = User(name=name, email=email, password=password)
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

    def update(self, db: Session, user_id: int, new_name: str = None, new_email: str = None, new_password: str = None) -> User | None:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return None
        
        if new_name is not None:
            user.name = new_name
        if new_email is not None:
            user.email = new_email
        if new_password is not None:
            user.password = new_password

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            return False

        db.delete(user)
        db.commit()
        return True