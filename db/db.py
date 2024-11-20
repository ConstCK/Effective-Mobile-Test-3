import json
from json import JSONDecodeError

from app.exceptions import DataError, DBError
from services.validators import ValidatorService


class DBEngine:
    """Сервис для операций с БД"""

    def __init__(self, name: str) -> None:
        self.name = name
        self.id = 1
        self.validator = ValidatorService()

    def get_all_data(self) -> list[str]:
        """Получение всех книг из базы данных"""
        with open(self.name, mode='r') as reader:
            try:
                data = reader.readlines()
                result = [json.loads(x) for x in data]

                print('!!!', result)
                print('???', type(result))

                return result
            except:
                return []

    def add_data(self, data: dict[str, str | int]) -> str:
        """Добавление информации в базу данных"""
        all_data = self.get_all_data()
        print('ALL', all_data)
        if not self.validator.validate_year(data.get('year')) or not self.validator.validate_text(
                data.get('title')) or not self.validator.validate_text(data.get('author')):
            raise DataError('Ввод некорректных данных')
        if self.validator.check_duplicates(data, all_data):
            raise DBError('Объект уже существует')
        print(data)
        data.update({'id': self.id, 'status': 'в наличии'})
        self.id += 1
        print(data)
        with open(self.name, mode='a') as writer:
            json.dump(data, writer)
        return 'Успешное добавление книги'

    def delete_data(self, book_id: int) -> str:
        """Удаление книги из базы данных"""
        all_data = self.get_all_data()
        if not self.validator.validate_id(book_id):
            raise DataError('Ввод некорректных данных')
        if not self.validator.check_if_exists(book_id, all_data):
            raise DBError('Объект не существует')
        result = list(filter(lambda item: item.get(id) != book_id, all_data))
        with open(self.name, mode='w') as writer:
            json.dump(result, writer)
        return 'Успешное удаление книги'

    def change_data(self, book_id: int) -> str:
        """Изменение статуса книги в базе данных"""
        all_data = self.get_all_data()
        if not self.validator.validate_id(book_id):
            raise DataError('Ввод некорректных данных')
        if not self.validator.check_if_exists(book_id, all_data):
            raise DBError('Объект не существует')
        book = list(filter(lambda item: book.get(id) == book_id, all_data))[0]
        book_index = all_data.index(book)
        book['status'] = 'в наличии' if book['status'] == 'выдана' else 'выдана'
        all_data[book_index] = book

        with open(self.name, mode='w') as writer:
            json.dump(all_data, writer)
        return 'Успешное изменение статуса книги'

    def get_books_by_title(self, title: str) -> list[dict[str, str | int]]:
        """Получение книг с указанным названием из базы данных"""
        all_data = self.get_all_data()
        if not self.validator.validate_text(title):
            raise DataError('Ввод некорректных данных')
        result = list(filter(lambda item: item.get('title') == title, all_data))
        return result

    def get_books_by_author(self, author: str) -> list[dict[str, str | int]]:
        """Получение книг с указанным названием из базы данных"""
        all_data = self.get_all_data()
        if not self.validator.validate_text(author):
            raise DataError('Ввод некорректных данных')
        result = list(filter(lambda item: item.get('title') == author, all_data))
        return result

    def get_books_by_year(self, year: int) -> list[dict[str, str | int]]:
        """Получение книг с указанным названием из базы данных"""
        all_data = self.get_all_data()
        if not self.validator.validate_year(year):
            raise DataError('Ввод некорректных данных')
        result = list(filter(lambda item: item.get('title') == year, all_data))
        return result
