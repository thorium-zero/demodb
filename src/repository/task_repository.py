import pyodbc
import itertools
from src.model.task import Task
from src.model.user import User
from src.repository.repository_base import RepositoryBase
from src.repository.user_repository import UserRepository


class TaskRepository(RepositoryBase):
    def __init__(self):
        super().__init__()
        self._table_name: str = "[task]"
        self._joint_table_name: str = "[taskuser]"
        self._model_type = Task
        self._user_repo: UserRepository = UserRepository()

    def __del__(self):
        super().__del__()

    def __check_task_and_user_exists(self, task_id: int, user_id: int) -> bool:
        task = self.find_by_id(task_id)
        user = self._user_repo.find_by_id(user_id)
        return task is not None and user is not None

    def add_responsible_user(self, task_id: int, user_id: int) -> bool:
        if not self.__check_task_and_user_exists(task_id, user_id):
            return False
        result = False
        cursor = self._db.cursor()
        try:
            cursor.execute(f"insert {self._joint_table_name}(task_id, user_id) values({task_id},{user_id})")
        except pyodbc.InternalError:
            pass
        else:
            result = cursor.rowcount > 0
            cursor.close()
            self._db.commit()
        return result

    def remove_responsible_user(self, task_id: int, user_id: int) -> bool:
        if not self.__check_task_and_user_exists(task_id, user_id):
            return False
        with self._db.cursor() as cursor:
            cursor.execute(f"delete from {self._joint_table_name} where task_id = {task_id} and user_id = {user_id}")
            result = cursor.rowcount > 0
            self._db.commit()
        return result

    def remove_all_responsible_users(self, task_id) -> bool:
        if not self.find_by_id(task_id):
            return False
        query = f"delete from {self._joint_table_name} where task_id = {task_id}"
        result = False
        with self._db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.rowcount > 0
            self._db.commit()
        return result

    def get_all_responsible_users(self, task_id: int) -> list[User]:
        if not self.find_by_id(task_id):
            return list()
        query = f"select user_id from {self._joint_table_name} where task_id = {task_id}"
        result = []
        with self._db.cursor() as cursor:
            cursor.execute(query)
            result.extend(self._user_repo.find_by_ids(tuple(itertools.chain.from_iterable(cursor.fetchall()))))
        return result
