from sqlalchemy.orm import Session
from repositories import CriteriaRepository
from models import Criteria
from dtos import CriteriaDTO

class CriteriaService:
    def __init__(self):
        self.repository = CriteriaRepository()

    def _is_name_invalid(self, name: str) -> bool:
        return len(name) == 0 or len(name) > 50

    def _is_description_invalid(self, description: str) -> bool:
        return len(description) > 500 or len(description) == 0

    def create_criteria(self, db: Session, name: str, description: str) -> CriteriaDTO:
        if self._is_name_invalid(name):
            raise ValueError("Nome de critério inválido")

        if self._is_description_invalid(description):
            raise ValueError("Descrição de critério inválida")

        criteria = Criteria(name=name, description=description)

        self.repository.create(db=db, criteria=criteria)

        return CriteriaDTO.from_entity(criteria)

    def list_criteria(self, db: Session) -> list[CriteriaDTO]:
        criteria_list = self.repository.get_all(db)

        return [
            CriteriaDTO(
                id=c.id, 
                name=c.name, 
                description=c.description
            ) 
            for c in criteria_list
        ]

    def get_criteria_by_id(self, db: Session, criteria_id: int) -> CriteriaDTO | None:
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return None
        
        return CriteriaDTO.from_entity(criteria)

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
            description=updated_criteria.description
            
        )

    def delete_criteria(self, db: Session, criteria_id: int) -> bool:
        criteria = self.repository.get_by_id(db, criteria_id)

        if criteria is None:
            return False
        
        return self.repository.delete(db, criteria)