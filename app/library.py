from db.db import DBEngine


class Library:
    def __init__(self, name: str, db_name: str) -> None:
        self.name = name
        self.db = DBEngine(db_name)


class Budget:
    def __init__(self, name: str, db_name: str, new: bool = False) -> None:
        self.validator = Validator()
        self.name = name
        self.db = db_name
        self.new = new
        if self.new:
            """Служебный запуск для создания пустой БД (для тестирования)"""
            with jsonlines.open(self.db, mode='w') as writer:
                data = {"id": 0, "name": self.name, "balance": 0, "spending": 0, "income": 0}
                self.id: int = 1
                writer.write(data)
            self.new = False
        else:
            """Служебный запуск для использования сервиса"""
            with jsonlines.open(self.db, mode='r') as reader:
                last_id = [item for item in reader][-1].get("id")
                self.id = last_id + 1

    def __str__(self) -> str:
        return f"личный финансовый кошелек пользователя: {self.name}"

    def get_all_data(self) -> list[dict]:
        """Получение всей информации из базы данных"""
        with jsonlines.open(self.db, mode="r") as reader:
            result = [item for item in reader]
            return result

    def get_meta(self) -> dict:
        """Отображение мета данных пользователя"""
        result = list(filter(lambda obj: obj.get("id") == 0, self.get_all_data()))[0]
        return result

    def get_data_by_category(self, mode: Literal["Доходы", "Расходы"]) -> list[dict] | list:
        """Получение информации из базы данных определенной категории """
        all_data = self.get_all_data()
        result = list(filter(lambda obj: obj.get("category") == mode, all_data[1:]))
        return result

    def get_data_by_date(self, year: str, month: str, day: str) -> list[dict] | list:
        """Получение информации из базы данных по дате"""
        all_data = self.get_all_data()
        result = list(filter(lambda obj: obj.get("date") == f"{year}-{month}-{day}", all_data[1:]))
        return result

    def get_data_by_sum(self,
                        amount: int,
                        mode: Literal["greater", "lower", "equal"] = "equal") -> list[dict] | list:
        """Получение информации из базы данных по сумме"""
        all_data = self.get_all_data()
        if mode == "greater":
            result = list(filter(lambda obj: int(obj.get('amount')) > amount, all_data[1:]))
        elif mode == "lower":
            result = list(filter(lambda obj: int(obj.get('amount')) < amount, all_data[1:]))
        elif mode == "equal":
            result = list(filter(lambda obj: int(obj.get('amount')) == amount, all_data[1:]))
        else:
            raise Exception("Ошибка режима")
        return result

    def add_data(self, data: dict, mode: Literal["Расходы", "Доходы"]) -> str:
        """Добавление информации в базу данных в зависимости от режима"""
        all_data = self.get_all_data()
        data = self.create_spending(data) if mode == "Расходы" else self.create_income(data)
        if self.validator.check_duplicates(data, all_data):
            return "Объект уже существует"
        self.change_balance(mode=mode, value=data.get("amount"))
        with jsonlines.open(self.db, mode="a") as writer:
            writer.write(data)
        return "Успешное добавление данных"

    def change_data(self, data_id: int, new_data: dict) -> str:
        """Изменение информации в базе данных"""
        result, updated_data, old_data = self.update_data(data_id=data_id, new_data=new_data)
        self.update_balance(all_data=result, new_data=updated_data, reserved_data=old_data)
        with jsonlines.open(self.db, mode="w") as writer:
            writer.write_all(result)
        return "Успешное изменение данных"

    def create_spending(self, data: dict) -> dict:
        """Создание записи с расходами (Вспомогательная функция)"""
        result = {"id": self.id, "category": "Расходы", "date": str(datetime.date.today())}
        result.update(data)
        self.id += 1
        if self.validator.validate_data(result):
            return result
        raise Exception("Некорректные данные")

    def create_income(self, data: dict) -> dict:
        """Создание записи с доходами (Вспомогательная функция)"""
        result = {"id": self.id, "category": "Доходы", "date": str(datetime.date.today())}
        result.update(data)

        self.id += 1
        if self.validator.validate_data(result):
            return result
        raise Exception("Некорректные данные")

    def update_data(self, data_id: int, new_data: dict) -> tuple[list[dict], dict, dict,]:
        """Изменение записи (Вспомогательная функция)"""
        all_data = self.get_all_data()
        if self.validator.check_if_exists(data_id, all_data):
            data: dict = list(filter(lambda obj: obj["id"] == data_id, all_data))[0]
        else:
            raise Exception("Указанного индекса не существует!")
        if self.validator.validate_data(new_data):
            reserved_data = data.copy()
            data.update(new_data)
            return all_data, data, reserved_data
        raise Exception("Некорректные данные")

    def change_balance(self, mode: Literal["Расходы", "Доходы"], value: int) -> None:
        """Изменение общего баланса при создании новой записи (Вспомогательная функция)"""
        all_data = self.get_all_data()
        meta: list[dict] = [i for i in all_data if i.get("id") == 0]
        balance: int = meta[0].get("balance")
        spending: int = meta[0].get("spending")
        income: int = meta[0].get("income")
        balance = balance + value if mode == "Доходы" else balance - value
        spending = spending + value if mode == "Расходы" else spending
        income = income + value if mode == "Доходы" else income
        meta[0].update({"balance": balance, "spending": spending, "income": income})
        with jsonlines.open(self.db, mode="w") as writer:
            writer.write_all(all_data)

    def update_balance(self, all_data: list[dict], new_data: dict, reserved_data: dict
                       ) -> None:
        """Изменение общего баланса при изменении записи (Вспомогательная функция)"""
        meta: list[dict] = [i for i in all_data if i.get("id") == 0]
        balance: int = meta[0].get("balance")
        spending: int = meta[0].get("spending")
        income: int = meta[0].get("income")
        print(reserved_data.get("amount"))
        print(new_data.get("amount"))
        if new_data.get("category") == "Доходы":
            income = income + new_data.get("amount") - reserved_data.get("amount")
            balance = balance + new_data.get("amount") - reserved_data.get("amount")
        elif new_data.get("category") == "Расходы":
            balance = balance - new_data.get("amount") + reserved_data.get("amount")
            spending = spending + new_data.get("amount") - reserved_data.get("amount")
        meta[0].update({"balance": balance, "spending": spending, "income": income})
        with jsonlines.open(self.db, mode="w") as writer:
            writer.write_all(all_data)
