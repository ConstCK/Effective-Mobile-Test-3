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
        print(f'Используйте ввод чисел (1-7) для навигации по меню')

    @staticmethod
    def show_menu() -> None:
        """Вывод всех команд меню в терминале"""
        print('1 - Завершение работы терминала')
        print('2 - Получение списка вех книг')
        print('3 - Получение списка книг с указанным названием')
        print('4 - Получение списка книг с указанным автором')
        print('5 - Получение списка книг указанного года')
        print('6 - Добавление книги в библиотеку')
        print('7 - Изменение статуса указанной книги')
        print('8 - Удаление указанной книги')

    def run_program(self) -> None:
        """Ввод команд меню для управления справочником"""
        while True:
            self.show_menu()
            choice = self.service.menu_choice_input()

            match choice:
                case 0:
                    print("Завершение программы...")
                    time.sleep(3)
                    break
                case 1:
                    print(self.get_meta_data())
                    print("*"*100)
                    time.sleep(1)
                case 2:
                    self.get_all_data()
                case 3:
                    self.get_categorized_data()
                case 4:
                    self.get_dated_data()
                case 5:
                    self.get_priced_data()
                case 6:
                    self.add_spending_data()
                case 7:
                    self.add_income_data()
                case 8:
                    self.change_data()

        print("Программа завершена!")