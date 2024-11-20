from app.library import Library
from services.validators import ValidatorService, PaginatorService


class Terminal:
    def __init__(self, library_name: str, db_name: str) -> None:
        self.library = Library(name=library_name, db_name=db_name)
        self.validator = ValidatorService()
        self.paginator = PaginatorService()

    def greetings(self) -> None:
        """Приветствие в терминале"""
        print(f'Добро пожаловать в библиотеку {self.library}')
        print(f'Используйте ввод чисел (1-7) для навигации по меню')
