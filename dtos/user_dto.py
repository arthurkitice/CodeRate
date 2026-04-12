# dtos/user_dto.py
from dataclasses import dataclass

@dataclass
class UserDTO:
    id: int
    name: str
    email: str

@dataclass
class CriteriaDTO:
    id: int
    name: str
    description: str
    user_id: int

@dataclass
class UserWithCriteriaDTO:
    id: int
    name: str
    email: str
    criteria: list[CriteriaDTO]