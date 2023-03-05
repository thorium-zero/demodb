from abc import ABC
from datetime import datetime

import pyodbc

from src.model.model_object import ModelObject


class RepositoryBase(ABC):
    __parameter_marker = "?"

    def __init__(self):
        connection_string = "Driver={SQL Server Native Client 11.0};Server=(localdb)\\MSSQLLocalDB;Database=task_manager;Trusted_Connection=yes;"
        self._db: pyodbc.Connection = pyodbc.connect(connection_string)
        self._table_name: str = ""
        self._model_type: ModelObject = None

    def __del__(self):
        if self._db:
            self._db.close()

    def add(self, obj: ModelObject) -> int:
        if not isinstance(obj, ModelObject):
            raise TypeError("Argument must be of the type ModelObject")
        cursor = self._db.cursor()
        obj_id = None
        query = f"insert {self._table_name}({','.join([f'{x}' for x in obj.fields[1:]])}) values({','.join([RepositoryBase.__parameter_marker for x in obj.values[1:]])})"
        try:
            cursor.execute(query, obj.values[1:])
        except pyodbc.DataError:
            pass
        except pyodbc.IntegrityError as er:
            print(f"Unable to insert new row {er.args}")
        else:
            obj_id = int(cursor.execute('select @@IDENTITY AS id;').fetchone()[0])
            if obj_id:
                self._db.commit()
        finally:
            cursor.close()
        return obj_id

    def remove(self, obj: ModelObject) -> bool:
        if not isinstance(obj, ModelObject):
            raise TypeError("Argument must be of the type ModelObject")
        if not isinstance(obj.id, int):
            return False
        query = f"delete from {self._table_name} where id = {obj.id}"
        with self._db.cursor() as cursor:
            cursor.execute(query)
        self._db.commit()
        return cursor.rowcount > 0

    def update(self, obj: ModelObject) -> bool:
        if not isinstance(obj, ModelObject):
            raise TypeError("Argument must be of the type ModelObject")
        new_data = ",".join([f"{cell} = {RepositoryBase.__parameter_marker}" for cell, value in tuple(obj)[1:]])
        query = f"update {self._table_name} set {new_data} where id = {RepositoryBase.__parameter_marker}"
        params = (*obj.values[1:], obj.values[0])
        with self._db.cursor() as cursor:
            cursor.execute(query, params)
        self._db.commit()
        return cursor.rowcount > 0

    def find_by_id(self, obj_id: int) -> ModelObject:
        query = f"select * from {self._table_name} where id = {obj_id}"
        with self._db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result is None:
            return None
        return self._model_type(*result)

    def find_by_ids(self, ids: tuple[int]) -> list[ModelObject]:
        ids_str = ",".join([f"{cid}" for cid in ids])
        query = f"select * from {self._table_name} where id in ({ids_str})"
        with self._db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        if result is None:
            return None
        return [self._model_type(*cobj) for cobj in result]

    def get_all(self) -> list:
        query = f"select * from {self._table_name}"
        with self._db.cursor() as cursor:
            cursor.execute(query)
            obj_tuples = cursor.fetchall()
        return [self._model_type(*obj) for obj in obj_tuples]

    def search(self, **kwargs) -> list:
        accepted_keys = (self._model_type.__dict__["__annotations__"].keys() | {"id": None}.keys()) & kwargs.keys()
        if (kwargs.keys() - accepted_keys) != set():
            raise KeyError("There are unacceptable arguments in the list of keys")
        filters = []
        for k in accepted_keys:
            if kwargs[k] is None:
                continue
            current = f"{k} = {kwargs[k]}" if not isinstance(kwargs[k], (str, datetime)) else f"{k} = '{kwargs[k]}'"
            filters.append(current)
        if len(filters) < 1:
            return []
        filters = " and ".join(filters)
        query = f"select * from {self._table_name} where {filters}"
        with self._db.cursor() as cursor:
            cursor.execute(query)
            result = [self._model_type(*obj_t) for obj_t in cursor.fetchall()]
        return result

    def clear(self):
        with self._db.cursor() as cursor:
            cursor.execute(f"delete from {self._table_name}")
