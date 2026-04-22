# dtos/user_dto.py
from dataclasses import dataclass
from dtos.criteria_dto import CriteriaDTO

@dataclass
class UserDTO:
    id: int
    name: str
    email: str

@dataclass
class UserWithCriteriaDTO:
    id: int
    name: str
    email: str
    criteria: list[CriteriaDTO]