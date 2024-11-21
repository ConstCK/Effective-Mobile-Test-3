from app.terminal import Terminal

app = Terminal(library_name='Effective-Mobile Library', db_name='db/data.json', )

with open('db/data.json', 'w'):
    pass

