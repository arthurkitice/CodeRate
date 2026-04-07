from sqlalchemy.orm import Session
from repositories.criteria_repository import CriteriaRepository
from services.user_service import UserService
from models import Criteria

class CriteriaService:
    def __init__(self):
        self.repository = CriteriaRepository()

    def _is_user_id_invalid(self, db: Session, user_id: int) -> bool:
        return UserService().get_user_by_id(db=db, user_id=user_id) is None

    def _is_name_invalid(self, name: str) -> bool:
        return len(name) == 0 or len(name) > 50

    def _is_description_invalid(self, description: str) -> bool:
        return len(description) > 500 or len(description) == 0

    def create_criteria(self, db: Session, name: str, description: str, user_id: int) -> Criteria:
        if self._is_user_id_invalid(db, user_id):
            raise ValueError("ID de usuário inválido")

        if self._is_name_invalid(name):
            raise ValueError("Nome de critério inválido")

        if self._is_description_invalid(description):
            raise ValueError("Descrição de critério inválida")

        criteria = Criteria(name=name, description=description, user_id=user_id)

        return self.repository.create(db=db, criteria=criteria)

    def list_criteria(self, db: Session) -> list[Criteria]:
        return self.repository.get_all(db)

    def get_criteria_by_id(self, db: Session, criteria_id: int) -> Criteria | None:
        return self.repository.get_by_id(db, criteria_id)
    
    def list_criteria_by_user_id(self, db: Session, user_id: int) -> list[Criteria]:
        return self.repository.list_by_user_id(db, user_id)

    def update_criteria(
        self,
        db: Session,
        criteria_id: int,
        new_name: str | None = None,
        new_description: str | None = None
    ) -> Criteria | None:
        
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return None

        if new_name is not None:
            if self._is_name_invalid(new_name):
                raise ValueError("Nome de critério inválido")
            criteria.name = new_name

        if new_description is not None:
            if self._is_description_invalid(new_description):
                raise ValueError("Descrição de critério inválida")
            criteria.description = new_description

        return self.repository.update(db, criteria)

    def delete_criteria(self, db: Session, criteria_id: int) -> bool:
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return False
        
        return self.repository.delete(db, criteria)