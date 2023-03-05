from src.model.user import User
from src.repository.repository_base import RepositoryBase


class UserRepository(RepositoryBase):
    def __init__(self):
        super().__init__()
        self._table_name = "[user]"
        self._model_type = User

    def __del__(self):
        super().__del__()
