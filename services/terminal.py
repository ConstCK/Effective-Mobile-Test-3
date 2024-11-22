from app.exceptions import DataError
from services.validators import ValidatorService


class TerminalService:
    def __init__(self) -> None:
        self.validator = ValidatorService()

    def menu_choice_input(self) -> int:
        """Сервис ввода номера операции меню терминала"""
        while True:
            try:
                choice = int(input('Введите номер операции: '))
                if self.validator.validate_menu_choice(choice):
                    return choice
                else:
                    print('Некорректный ввод номера операции (должно быть число от 1 до 8)')
            except ValueError:
                print('Ошибка ввода. Введите число (1-8)')

    def id_input(self) -> int:
        """Сервис ввода id"""
        while True:
            book_id = input("Введите id книги: ")
            try:
                book_id = int(book_id)
                if self.validator.validate_id(book_id):
                    return book_id
                print("Некорректный ввод id")
            except ValueError:
                print("Некорректный ввод id")

    def title_input(self) -> str:
        """Сервис ввода названия книги"""
        while True:
            book_title = input("Введите название книги: ")
            if self.validator.validate_text(book_title):
                return book_title
            print("Некорректное название книги")

    def author_input(self) -> str:
        """Сервис ввода автора книги"""
        while True:
            book_author = input("Введите автора книги: ")
            if self.validator.validate_text(book_author):
                return book_author.title().strip()
            print("Некорректный автор книги")

    def year_input(self) -> int:
        """Сервис ввода года книги"""
        while True:
            book_year = input("Введите год публикации книги: ")
            try:
                book_year = int(book_year)
                if self.validator.validate_year(book_year):
                    return book_year

                print('Некорректный ввод года')
            except ValueError:
                print('Некорректный ввод года')

    @staticmethod
    def page_input() -> bool:
        """Сервис продолжения/выхода из подменю"""
        while True:
            choice = input("Введите число (1 - для продолжения / 0 - для выхода): ")
            if choice == "1":
                return True
            elif choice == "0":
                return False
            else:
                print("Некорректный ввод (должно быть 1 или 0)")

    @staticmethod
    def books_representation(books):
        """Представление книги"""
        for item in next(books):
            print('*' * 100)
            print(f'Книга №{item['id']}.')
            print(f'Книга "{item['title']}", автор: {item['author']}, печать: {item['year']} г.')
            print(f'Статус книги: {item['status']}.')
            print('*' * 100)
