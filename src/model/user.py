from dataclasses import dataclass

from src.model.model_object import ModelObject


@dataclass
class User(ModelObject):
    login: str
    pass_hash: bytes
    last_name: str
    first_name: str
    email: str
