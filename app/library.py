from db.db import DBEngine


class Library:
    def __init__(self, name: str, db_name: str) -> None:
        self.name = name
        self.db = DBEngine(db_name)

    def get_all_book(self) -> list[dict[str, str | int]]:
        """Метод для получения всех книг библиотеки"""
        return self.db.get_all_data()

    def get_book_by_title(self, title: str) -> list[dict[str, str | int]]:
        """Метод для получения книг из библиотеки с указанным названием"""
        return self.db.get_books_by_title(title=title)

    def get_book_by_author(self, author: str) -> list[dict[str, str | int]]:
        """Метод для получения книг из библиотеки указанного автора"""
        return self.db.get_books_by_author(author=author)

    def get_book_by_year(self, year: int) -> list[dict[str, str | int]]:
        """Метод для получения книг из библиотеки указанного года"""
        return self.db.get_books_by_year(year=year)

    def delete_book(self, book_id: int) -> str:
        """Метод для удаления книги из библиотеки с указанным id"""
        return self.db.delete_data(book_id=book_id)

    def change_book_status(self, book_id: int) -> str:
        """Метод для изменения статуса книги (на противоположный) в библиотеке с указанным id"""
        return self.db.change_data(book_id=book_id)

    def add_book(self, data: dict[str, str | int]) -> str:
        """Метод для добавления книги в библиотеку"""
        return self.db.add_data(data=data)
