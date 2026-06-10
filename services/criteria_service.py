from repositories import CriteriaRepository
from models import Criteria
from dtos import CriteriaDTO
from database import get_db

class CriteriaService:
    def __init__(self):
        self.repository = CriteriaRepository()

    def _is_name_invalid(self, name: str) -> bool:
        return len(name) == 0 or len(name) > 50

    def _is_description_invalid(self, description: str) -> bool:
        return len(description) > 4500 or len(description) == 0

    def create_criteria(self, name: str, description: str) -> CriteriaDTO:
        if self._is_name_invalid(name):
            raise ValueError("Nome de critério inválido")

        if self._is_description_invalid(description):
            raise ValueError("Descrição de critério inválida")

        criteria = Criteria(name=name, description=description)

        with get_db() as db:
            self.repository.create(db=db, criteria=criteria)
            return CriteriaDTO.from_entity(criteria)

    def list_criteria(self) -> list[CriteriaDTO]:
        with get_db() as db:
            criteria_list = self.repository.get_all(db)
            return [CriteriaDTO.from_entity(c) for c in criteria_list]

    def get_criteria_by_id(self, criteria_id: int) -> CriteriaDTO | None:
        with get_db() as db:
            criteria = self.repository.get_by_id(db, criteria_id)
            if criteria is None:
                return None
            return CriteriaDTO.from_entity(criteria)

    def update_criteria(
        self,
        criteria_id: int,
        new_name: str | None = None,
        new_description: str | None = None
    ) -> CriteriaDTO | None:
        
        with get_db() as db:
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
            return CriteriaDTO.from_entity(updated_criteria)

    def delete_criteria(self, criteria_id: int) -> bool:
        with get_db() as db:
            criteria = self.repository.get_by_id(db, criteria_id)
            if criteria is None:
                return False
            return self.repository.delete(db, criteria)