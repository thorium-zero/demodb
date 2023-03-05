import msvcrt
import re
import os
from subprocess import call
from datetime import datetime


class Console:
    @staticmethod
    def read_key(message="Press any key to continue") -> str:
        print(message, end="")
        return msvcrt.getwch()

    @staticmethod
    def read_line(message="[Expecting a string] >>> ") -> str:
        return input(message)

    @staticmethod
    def read_date(message="[Date format: dd.mm.yyyy] >>> ") -> datetime:
        template = r"(\d+)[\.\- \\/](\d+)[\.\- \\/](\d+)"
        flag = True
        result = None
        while flag:
            print(message, end="")
            string = input()
            date_raw = re.search(template, string)
            if len(groups := date_raw.groups()) < 3:
                continue
            if len(groups[2]) < 4:
                print("year must me in XXXX format")
                continue
            try:
                result = datetime(int(groups[2]), int(groups[1]), int(groups[0]))
            except ValueError as er:
                print(er.args[0])
            if result is not None:
                flag = False
        return result

    @staticmethod
    def read_int(message="Expecting an integer >>> "):
        while True:
            print(message, end="")
            string = input()
            try:
                if string.isalnum():
                    return int(string)
            except ValueError as er:
                pass
            print(f"{string} is not a valid integer")

    @staticmethod
    def clear():
        call('clear' if os.name == 'posix' else 'cls')
