from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models import User
import hashlib


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _email_already_exists(self, db: Session, email: str) -> bool:
        existing_user = self.repository.get_by_email(db, email)
        return existing_user is not None

    def authenticate_user(self, db: Session, email: str, password: str) -> User:
        user = self.repository.get_by_email(db, email)

        if user is None:
            raise ValueError("Email não encontrado")

        hashed_password = self._hash_password(password)

        if user.password != hashed_password:
            raise ValueError("Senha incorreta")

        return user

    def create_user(self, db: Session, name: str, email: str, password: str) -> User:
        if self._email_already_exists(db, email):
            raise ValueError("Email já cadastrado")

        hashed_password = self._hash_password(password)

        user = User(name=name, email=email, password=hashed_password)

        return self.repository.create(db=db, user=user)

    def list_users(self, db: Session) -> list[User]:
        return self.repository.get_all(db)

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return self.repository.get_by_id(db, user_id)

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return self.repository.get_by_email(db, email)

    def update_user(
        self,
        db: Session,
        user_id: int,
        new_name: str | None = None,
        new_email: str | None = None,
        new_password: str | None = None
    ) -> User | None:
        
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return None

        if new_name is not None:
            user.name = new_name

        if new_email is not None:
            if self._email_already_exists(db, new_email) and user.email != new_email:
                raise ValueError("Email já cadastrado")
            user.email = new_email

        if new_password is not None:
            hashed_password = self._hash_password(new_password)
            user.password = hashed_password

        return self.repository.update(user)

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return False
        
        return self.repository.delete(db, user)