from src.menu import Menu
from src.model.user import User
from src.repository.task_repository import TaskRepository
from src.repository.user_repository import UserRepository
from src.utility.console import Console
from src.utility.pass_tool import PassTool


class Application:
    def __init__(self):
        self._current_user: User = None
        self._user_repo: UserRepository = UserRepository()
        self._task_repo: TaskRepository = TaskRepository()

    def __login(self) -> bool:
        login: str = Console.read_line("login >>> ")
        password: str = Console.read_line("password >>> ")
        users: list[User] = self._user_repo.search(login=login)
        if len(users) != 1:
            print("user not found")
            return False
        if PassTool.check_password(password, users[0].pass_hash):
            self._current_user = users[0]
            return True
        return False

    def __register(self) -> bool:
        login: str = Console.read_line("login >>> ")
        password: str = Console.read_line("password >>> ")
        if len(self._user_repo.search(login=login)) > 0:
            print("login is taken")
            return False
        last_name: str = Console.read_line("last name >>> ")
        first_name: str = Console.read_line("first name >>> ")
        while True:
            email: str = Console.read_line("email >>> ")
            if len(self._user_repo.search(email=email)) == 0:
                break
            print("this email is taken, use another one")
        return self._user_repo.add(User(0, login, PassTool.make_hash(password), last_name, first_name, email)) != 0

    def _start_up(self):
        start_up_process = True
        while start_up_process:
            pass

    def run(self):
        root_menu = Menu()
        root_menu.add_menu_item("login", 1)
        root_menu.add_menu_item("register", 2)
        root_menu.add_menu_item("exit", 3)
        main_menu = Menu()
        main_menu.add_menu_item("show all my tasks", None)
        main_menu.add_menu_item("show all tasks by user", None)
        main_menu.add_menu_item("show all unfinished tasks", None)
        main_menu.add_menu_item("show all tasks by date", None)
        main_menu.add_menu_item("show all tasks by responsible user", None)
        main_menu.add_menu_item("show all unassigned tasks", None)
        main_menu.add_menu_item("show all free users", None)
        main_menu.add_menu_item("create new task", None)
        main_menu.add_menu_item("assign a task", None)
        main_menu.add_menu_item("remove a task", None)
        main_menu.add_menu_item("modify a task", None)
        main_menu.add_menu_item("move one level up", None)
