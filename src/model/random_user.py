# python -m pip install faker
from dataclasses import dataclass
import datetime
from faker import Faker


@dataclass
class RandomUser:
    login: str
    first_name: str
    last_name: str
    phone_number: str
    email: str
    birth_date: datetime

    @staticmethod
    def generate():
        _rd_provider = Faker(locale='en_US')
        first_name = _rd_provider.first_name_male()
        last_name = _rd_provider.last_name_male()
        login = f"{last_name}{_rd_provider.pyint(100)}".lower()
        pcode = ["050", "063", "066", "067", "068", "093", "095", "096", "097"]
        pbody = str(_rd_provider.pyint(1000000, 9999999))
        phone_number = f"+38({pcode[_rd_provider.pyint(0, len(pcode))]}){pbody[:3]}-{pbody[3:5]}-{pbody[5:]}"
        email = f"{login}@{_rd_provider.free_email_domain()}".lower()
        birth_date = _rd_provider.date_of_birth(None, 15, 60)
        return RandomUser(login, first_name, last_name, phone_number, email, birth_date)

    def __str__(self) -> str:
        return f"{'Last Name':10}: {self.last_name}\n{'First Name':10}: {self.first_name}\n{'Birthday':10}: {self.birth_date}\n{'Login':10}: {self.login}\n{'Email':10}: {self.email}\n{'Phone':10}: {self.phone_number}"
