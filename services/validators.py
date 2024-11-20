import datetime


class ValidatorService:
    """
    Сервис для валидации вводимых данных
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_id(book_id: int) -> bool:
        """Валидация вводимого id книги"""
        return book_id > 0 and isinstance(book_id, int)

    @staticmethod
    def validate_text(text: str) -> bool:
        """Валидация вводимого названия книги или автора"""
        return len(text) > 1

    @staticmethod
    def validate_year(year: int) -> bool:
        """Валидация вводимого года книги"""
        now = datetime.datetime.now().year
        print('123', type(now))
        return now > year > 1900 and isinstance(year, int)

    @staticmethod
    def check_duplicates(data: dict, all_books: list[dict[str, str | int]]) -> bool:
        """Проверка вводимой книги на дубликат"""
        if all_books:
            result = any([True if (
                    data['title'] == book.get('title') and data['author'] == book.get('author') and data[
                'year'] == book.get(
                'year')) else False for book in all_books])
            return result
        return False

    @staticmethod
    def check_if_exists(data_id: int, all_data: list[dict[str, str | int]]) -> bool:
        """Проверка на существование книги с указанным id"""
        if all_data:
            result = any([True if data_id == book.get("id") else False for book in all_data[1:]])
            return result
        return False

    @staticmethod
    def validate_menu_choice(menu_id: int) -> bool:
        """Валидация вводимых данных (номер операции меню)"""
        return 9 > menu_id >= 0 and isinstance(menu_id, int)


class PaginatorService:
    pass
