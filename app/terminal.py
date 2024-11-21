import time

from app.exceptions import DBError
from app.library import Library
from services.paginator import PaginatorService
from services.terminal import TerminalService
from services.validators import ValidatorService


class Terminal:
    def __init__(self, library_name: str, db_name: str) -> None:
        self.library = Library(name=library_name, db_name=db_name)
        self.validator = ValidatorService()
        self.paginator = PaginatorService()
        self.service = TerminalService()

    def greetings(self) -> None:
        """Приветствие в терминале"""
        print(f'Добро пожаловать в библиотеку {self.library}')

    @staticmethod
    def show_menu() -> None:
        """Вывод всех команд меню в терминале"""
        print(f'Используйте ввод чисел (1-8) для навигации по меню')
        print('1 - Завершение работы терминала')
        print('2 - Получение списка вех книг')
        print('3 - Получение списка книг с указанным названием')
        print('4 - Получение списка книг с указанным автором')
        print('5 - Получение списка книг указанного года')
        print('6 - Добавление книги в библиотеку')
        print('7 - Изменение статуса указанной книги')
        print('8 - Удаление указанной книги')

    def _show_all_books(self) -> None:
        """Вывод всех книг библиотеки"""
        data = self.library.get_all_books()
        result = self.paginator.paginate_data(data)
        go_ahead = True
        while go_ahead:
            try:
                print('Список всех книг')
                self.service.books_representation(result)

            except StopIteration:
                print("Данных больше нет...")
                break
            go_ahead = self.service.page_input()
        print('Выход из режима показа всех книг...')

    def _show_books_by_title(self, book_title) -> None:
        """Вывод книг библиотеки с указанным названием"""
        data = self.library.get_books_by_title(book_title)
        result = self.paginator.paginate_data(data)
        go_ahead = True
        while go_ahead:
            try:
                print(f'Список книг. Название: {book_title}')
                self.service.books_representation(result)

            except StopIteration:
                print("Данных больше нет...")
                break
            go_ahead = self.service.page_input()
        print(f'Выход из режима показа книг {book_title}...')

    def _show_books_by_author(self, book_author) -> None:
        """Вывод книг библиотеки с указанным автором"""
        data = self.library.get_books_by_author(book_author)
        result = self.paginator.paginate_data(data)
        go_ahead = True
        while go_ahead:
            try:
                print(f'Список книг. Автор: {book_author}')
                self.service.books_representation(result)

            except StopIteration:
                print("Данных больше нет...")
                break
            go_ahead = self.service.page_input()
        print(f'Выход из режима показа книг автора {book_author}...')

    def _show_books_by_year(self, book_year) -> None:
        """Вывод книг библиотеки с указанным годом публикации"""
        data = self.library.get_books_by_year(book_year)
        result = self.paginator.paginate_data(data)
        go_ahead = True
        while go_ahead:
            try:
                print(f'Список книг. Публикация: {book_year} г.')
                self.service.books_representation(result)

            except StopIteration:
                print("Данных больше нет...")
                break
            go_ahead = self.service.page_input()
        print(f'Выход из режима показа книг публикации {book_year} г....')

    def run_program(self) -> None:
        """Ввод команд меню для управления библиотекой"""
        while True:
            self.show_menu()
            choice = self.service.menu_choice_input()

            match choice:
                case 1:
                    print("Завершение программы...")
                    time.sleep(2)
                    break
                case 2:
                    self._show_all_books()
                    time.sleep(1)
                case 3:
                    book_title = self.service.title_input()
                    self._show_books_by_title(book_title)
                    time.sleep(1)
                case 4:
                    book_author = self.service.author_input()
                    self._show_books_by_author(book_author)
                    time.sleep(1)
                case 5:
                    book_year = self.service.year_input()
                    self._show_books_by_year(book_year)
                    time.sleep(1)
                case 6:
                    book_title = self.service.title_input()
                    book_author = self.service.author_input()
                    book_year = self.service.year_input()
                    data = {'title': book_title, 'author': book_author, 'year': book_year}
                    try:
                        print(self.library.add_book(data))
                        print("*" * 100)
                        time.sleep(1)
                    except DBError as error:
                        print(error)
                case 7:
                    book_id = self.service.id_input()
                    try:
                        print(self.library.change_book_status(book_id))
                        print("*" * 100)
                        time.sleep(1)
                    except DBError as error:
                        print(error)
                case 8:
                    book_id = self.service.id_input()
                    try:
                        print(self.library.delete_book(book_id))
                        print("*" * 100)
                        time.sleep(1)
                    except DBError as error:
                        print(error)

        print("Программа завершена!")
