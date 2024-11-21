from app.library import Library

library_test = Library(name='Effective-Mobile Library test', db_name='tests/test.json')


def test_get_initial_data():
    """Тест Получения данных из пустой БД"""
    assert library_test.get_all_books() == []
