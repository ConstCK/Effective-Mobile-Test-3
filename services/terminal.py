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
                    print('Некорректный ввод номера операции (должно быть число от 0 до 8)')
            except ValueError:
                print('Ошибка ввода. Введите число (0-8)')
