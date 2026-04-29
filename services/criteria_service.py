from sqlalchemy.orm import Session
from repositories import CriteriaRepository
from services.user_service import UserService
from models import Criteria
from dtos import CriteriaDTO

class CriteriaService:
    def __init__(self):
        self.repository = CriteriaRepository()

    def _is_user_id_invalid(self, db: Session, user_id: int) -> bool:
        return UserService().get_user_by_id(db=db, user_id=user_id) is None

    def _is_name_invalid(self, name: str) -> bool:
        return len(name) == 0 or len(name) > 50

    def _is_description_invalid(self, description: str) -> bool:
        return len(description) > 500 or len(description) == 0

    def create_criteria(self, db: Session, name: str, description: str, user_id: int) -> CriteriaDTO:
        if self._is_user_id_invalid(db, user_id):
            raise ValueError("ID de usuário inválido")

        if self._is_name_invalid(name):
            raise ValueError("Nome de critério inválido")

        if self._is_description_invalid(description):
            raise ValueError("Descrição de critério inválida")

        criteria = Criteria(name=name, description=description, user_id=user_id)

        self.repository.create(db=db, criteria=criteria)

        return CriteriaDTO.from_entity(criteria)

    def list_criteria(self, db: Session) -> list[CriteriaDTO]:
        criteria_list = self.repository.get_all(db)

        return [
            CriteriaDTO(
                id=c.id, 
                name=c.name, 
                description=c.description, 
                user_id=c.user_id
            ) 
            for c in criteria_list
        ]

    def get_criteria_by_id(self, db: Session, criteria_id: int) -> CriteriaDTO | None:
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return None
        
        return CriteriaDTO.from_entity(criteria)
    
    def list_criteria_by_user_id(self, db: Session, user_id: int) -> list[CriteriaDTO]:
        criteria_list = self.repository.list_by_user_id(db, user_id)
        return [
            CriteriaDTO(
                id=c.id, 
                name=c.name, 
                description=c.description, 
                user_id=c.user_id
            ) 
            for c in criteria_list
        ]

    def update_criteria(
        self,
        db: Session,
        criteria_id: int,
        new_name: str | None = None,
        new_description: str | None = None
    ) -> CriteriaDTO | None:
        
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

        updated_criteria = self.repository.update(db, criteria)

        return CriteriaDTO(
            id = updated_criteria.id,
            name = updated_criteria.name,
            description=updated_criteria.description,
            user_id=updated_criteria.user_id
        )

    def delete_criteria(self, db: Session, criteria_id: int) -> bool:
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return False
        
        return self.repository.delete(db, criteria)