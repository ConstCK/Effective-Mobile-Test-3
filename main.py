from db.db import DBEngine
main = DBEngine('db/data.json')

with open('db/data.json', 'w'):
    pass
main.add_data({'title': 'name 1', 'author': 'Pushkin', 'year': 1985})
main.add_data({'title': 'name 2', 'author': 'Pushkin', 'year': 1995})
main.add_data({'title': 'name 3', 'author': 'Lermontov', 'year': 1995})
main.add_data({'title': 'name 4', 'author': 'Lermontov', 'year': 2000})
main.add_data({'title': 'name 5', 'author': 'Dontsova', 'year': 2000})
main.add_data({'title': 'name 1', 'author': 'Pushkin', 'year': 1985})
main.change_data(book_id=1)
main.delete_data(book_id=2)
print(main.get_books_by_author('Lermontova'))
print(main.get_books_by_title('name 1'))
print(main.get_books_by_year(2000))
