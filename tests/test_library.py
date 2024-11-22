import pytest

from app.exceptions import DBError, DataError
from app.library import Library

library_test = Library(name='Effective-Mobile Library test', db_name='tests/test.json')


@pytest.fixture(scope='function')
def test_clear_db():
    with open('tests/test.json', 'w'):
        pass


def test_get_initial_data(test_clear_db):
    """Тест получения данных из пустой БД"""
    assert library_test.get_all_books() == []


@pytest.mark.parametrize('data, expected', [({'title': 'Руслан и Людмила',
                                              'author': 'А.С.Пушкин',
                                              'year': 1985}, 'Успешное добавление книги'),
                                            ({'title': 'Сказка о рыбаке...',
                                              'author': 'А.С.Пушкин',
                                              'year': 1995}, 'Успешное добавление книги'),
                                            ({'title': 'Вечера на хуторе...',
                                              'author': 'Н.В.Гоголь',
                                              'year': 1985}, 'Успешное добавление книги'),
                                            ({'title': 'Вий',
                                              'author': 'Н.В.Гоголь',
                                              'year': 1995}, 'Успешное добавление книги'),
                                            ({'title': 'Вий',
                                              'author': 'Н.В.Гоголь',
                                              'year': 2000}, 'Успешное добавление книги'),
                                            ])
def test_add_books(data, expected):
    """Тест успешного добавления книг в БД"""
    assert library_test.add_book(data) == expected


@pytest.mark.parametrize('data', [({'title': 'Руслан и Людмила',
                                    'author': 'А.С.Пушкин',
                                    'year': 1985}),
                                  ])
def test_add_duplicate_books(data):
    """Тест добавления дубликата книги в БД"""
    with pytest.raises(DBError):
        library_test.add_book(data)


def test_get_all_books():
    """Тест получения всех книг из БД"""
    assert len(library_test.get_all_books()) == 5


def test_get_books_by_title():
    """Тест получения книг с указанным названием из БД"""
    assert len(library_test.get_books_by_title('Вий')) == 2


def test_get_books_by_author():
    """Тест получения книг указанного автора из БД"""
    assert len(library_test.get_books_by_author('Н.В.Гоголь')) == 3


def test_get_books_by_year():
    """Тест получения книг указанного года из БД"""
    assert len(library_test.get_books_by_year(1985)) == 2


def test_get_books_by_wrong_year():
    """Тест получения книг с указанием неправильного года из БД"""
    with pytest.raises(DataError):
        library_test.get_books_by_year(2500)


def test_change_book_status():
    """Тест изменения статуса книги с указанным id из БД"""
    book_id = library_test.get_all_books()[0]['id']
    assert library_test.change_book_status(book_id) == 'Успешное изменение статуса книги'


def test_change_wrong_book_status():
    """Тест изменения статуса несуществующей книги с указанным id из БД"""
    book_id = 1000000
    with pytest.raises(DBError):
        library_test.change_book_status(book_id)


def test_delete_book():
    """Тест удаления книги с указанным id из БД"""
    book_id = library_test.get_all_books()[-1]['id']
    assert library_test.delete_book(book_id) == 'Успешное удаление книги'


def test_delete_wrong_book():
    """Тест удаления книги с несуществующим id из БД"""
    book_id = 100000
    with pytest.raises(DBError):
        library_test.delete_book(book_id)


def test_get_books():
    """Тест повторного получения всех книг из БД"""
    assert len(library_test.get_all_books()) == 4
