from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models import User
from dtos.user_dto import UserDTO, UserWithCriteriaDTO, CriteriaDTO
import bcrypt


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def _verify_password(self, password: str, hashed: str) -> str:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def _email_already_exists(self, db: Session, email: str) -> bool:
        existing_user = self.repository.get_by_email(db, email)
        return existing_user is not None

    def authenticate_user(self, db: Session, email: str, password: str) -> UserDTO:
        user = self.repository.get_by_email(db, email)

        if user is None:
            raise ValueError("Email não encontrado")

        if not self._verify_password(password, user.password):
            raise ValueError("Senha incorreta")

        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email
        )

    def create_user(self, db: Session, name: str, email: str, password: str) -> UserDTO:
        if len(name) == 0:
            raise ValueError("Nome não pode ser vazio")
        elif len(name) > 25: 
            raise ValueError("Nome deve ter no máximo 25 caracteres")

        if self._email_already_exists(db, email):
            raise ValueError("Email já cadastrado")

        hashed_password = self._hash_password(password)

        user = User(name=name, email=email, password=hashed_password)

        self.repository.create(db, user)

        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email
        )

    def list_users(self, db: Session) -> list[UserDTO]:
        users = self.repository.get_all(db)
        return [
            UserDTO(id=u.id, name=u.name, email=u.email) 
            for u in users
        ]

    def get_user_by_id(self, db: Session, user_id: int) -> UserDTO | None:
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return None

        return UserDTO(id = user.id, name=user.name, email=user.email)

    def get_user_by_email(self, db: Session, email: str) -> UserDTO | None:
        user = self.repository.get_by_email(db, email)

        if user is None:
            return None
        
        return UserDTO(id = user.id, name=user.name, email=user.email)

    def get_user_with_criteria(self, db: Session, user_id: int) -> UserWithCriteriaDTO | None:
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return None
        
        criteria_list = [
            CriteriaDTO(
                id=c.id, 
                name=c.name, 
                description=c.description, 
                user_id=user.id
            ) 
            for c in user.criteria
        ]

        return UserWithCriteriaDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            criteria=criteria_list
        )

    def update_user(
        self,
        db: Session,
        user_id: int,
        new_name: str | None = None,
        new_email: str | None = None,
        new_password: str | None = None
    ) -> UserDTO | None:
        
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return None

        if new_name is not None:
            user.name = new_name

        if new_email is not None:
            invalid_email = self._email_already_exists(db, new_email) and user.email != new_email
            if invalid_email:
                raise ValueError("Email já cadastrado")
            user.email = new_email

        if new_password is not None:
            hashed_password = self._hash_password(new_password)
            user.password = hashed_password
        
        updated_user = self.repository.update(db, user)

        return UserDTO(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email
        )

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = self.repository.get_by_id(db, user_id)

        if user is None:
            return False
        
        return self.repository.delete(db, user)