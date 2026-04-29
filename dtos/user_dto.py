# dtos/user_dto.py
from pydantic import BaseModel, EmailStr
from dtos.criteria_dto import CriteriaDTO
from models import User

class UserDTO(BaseModel):
    id: int
    name: str
    email: str

    @classmethod
    def from_entity(cls, user: User) -> "UserDTO":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email
        )

class UserWithCriteriaDTO(BaseModel):
    id: int
    name: str
    email: str
    criteria: list[CriteriaDTO]

    @classmethod
    def from_entity(cls, user: User) -> "UserWithCriteriaDTO":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            criteria=[CriteriaDTO.from_entity(c) for c in user.criteria]
        )