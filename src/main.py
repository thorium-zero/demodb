from datetime import datetime

from src.application import Application
from src.model.task import Task
from src.repository.task_repository import TaskRepository
from src.repository.user_repository import UserRepository
from src.utility.console import Console
from src.utility.pass_tool import PassTool

"""
    name: str
    priority: bool
    description: str
    execution_date: datetime
    task_completed: bool = False
"""


def main():
    # t0 = Task(0, "Купить картошку", False, "Кончилась картошка, не с чего суп делать", datetime.now(), True)
    # t1 = Task(0, "Вынести мусор", True, "Уже воняет, надо выкинуть", datetime.now(), False)
    # t2 = Task(0, "Забрать детё со школы", False, "Ато вернется завтра", datetime(2023, 2, 27), False)
    # t3 = Task(0, "Выполнить задание по программированию", True, "Доделать второй уровень", datetime(2023, 3, 13), False)
    # t4 = Task(0, "Работа над ошибками", True, "Исправить баг в системе логирования", datetime(2023, 2, 27), False)
    #
    # tr = TaskRepository()
    # tr.add(t0)
    # tr.add(t1)
    # tr.add(t2)
    # tr.add(t3)
    # tr.add(t4)
    #
    # tr.search(task_completed=True)
    # tr.search(priority=True)
    pass


if __name__ == "__main__":
    main()
