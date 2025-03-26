import pickle
from datetime import datetime
import builtins
import atexit


class PharmacyError(Exception):
    """Базовое исключение для аптеки"""
    pass


class InvalidMedicineError(PharmacyError):
    """Исключение при недопустимых значениях лекарства"""

    def __init__(self, field, value):
        self.field = field
        self.value = value
        super().__init__(f"Недопустимое значение {field}: {value}")


class OperationNotAllowedError(PharmacyError):
    """Исключение при попытке недопустимой операции"""

    def __init__(self, operation):
        super().__init__(f"Операция '{operation}' не разрешена")


class Medicine:
    """Класс для описания лекарства в аптеке."""

    __next_id = 1

    def __init__(self, name="Неизвестно", price=0, quantity=0, expiry_date="2023-12-31"):
        self.__id = Medicine.__next_id
        Medicine.__next_id += 1
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__expiry_date = expiry_date
        self.__transactions = []
        atexit.register(self._safe_close)

        # Валидация при создании
        if price < 0:
            raise InvalidMedicineError("цена", price)
        if quantity < 0:
            raise InvalidMedicineError("количество", quantity)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise InvalidMedicineError("название", value)
        self.__name = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise InvalidMedicineError("цена", value)
        self.__price = value

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidMedicineError("количество", value)
        self.__quantity = value

    @property
    def expiry_date(self):
        return self.__expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        if not isinstance(value, str):
            raise InvalidMedicineError("срок годности", value)
        self.__expiry_date = value

    def _safe_close(self):
        """Безопасное закрытие с записью в лог."""
        try:
            with builtins.open('medicine_deleted.log', 'a') as f:
                f.write(f'{datetime.now()}: Удалено лекарство {self.__name} (ID: {self.__id})\n')
                f.flush()
        except Exception as e:
            print(f"Ошибка при записи лога лекарства: {e}")

    def __del__(self):
        self._safe_close()

    def __str__(self):
        return (f"Лекарство #{self.__id}: {self.__name}, Цена: {self.__price} руб., "
                f"Количество: {self.__quantity}, Годен до: {self.__expiry_date}")

    def sell(self, amount=1):
        if amount <= 0:
            raise InvalidMedicineError("количество для продажи", amount)

        if self.__quantity < amount:
            raise OperationNotAllowedError(f"Недостаточно товара (доступно: {self.__quantity}, запрошено: {amount})")

        old_quantity = self.__quantity
        self.__quantity -= amount
        self.__log_transaction('Продажа', old_quantity, self.__quantity, amount)
        return True

    def restock(self, amount=1):
        if amount <= 0:
            raise InvalidMedicineError("количество для пополнения", amount)

        old_quantity = self.__quantity
        self.__quantity += amount
        self.__log_transaction('Пополнение', old_quantity, self.__quantity, amount)

    def __log_transaction(self, operation, old_value, new_value, amount):
        transaction = {
            'datetime': datetime.now(),
            'operation': operation,
            'old_value': old_value,
            'new_value': new_value,
            'amount': amount
        }
        self.__transactions.append(transaction)

    def get_transactions(self):
        return self.__transactions.copy()


class Pharmacy:
    """Класс для управления ассортиментом аптеки."""

    def __init__(self, name="Аптека"):
        self.__name = name
        self.__medicines = []
        self.__transactions = []
        atexit.register(self._safe_close)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise InvalidMedicineError("название аптеки", value)
        self.__name = value

    @property
    def medicines(self):
        return self.__medicines.copy()

    def _safe_close(self):
        """Безопасное закрытие с записью в лог."""
        try:
            with builtins.open('pharmacy_deleted.log', 'a') as f:
                f.write(f'{datetime.now()}: Удалена аптека {self.__name}\n')
                f.flush()
        except Exception as e:
            print(f"Ошибка при записи лога аптеки: {e}")

    def __del__(self):
        self._safe_close()

    def __str__(self):
        return f"{self.__name}. Лекарств в ассортименте: {len(self.__medicines)}"

    def add_medicine(self, medicine):
        if not isinstance(medicine, Medicine):
            raise InvalidMedicineError("тип лекарства", type(medicine))

        self.__medicines.append(medicine)
        self.__log_transaction('Добавление лекарства', None, None, medicine.name)
        return f"Добавлено: {medicine.name}"

    def __log_transaction(self, operation, old_value, new_value, details):
        transaction = {
            'datetime': datetime.now(),
            'operation': operation,
            'details': details
        }
        self.__transactions.append(transaction)

    def get_transactions(self):
        return self.__transactions.copy()

    def save_to_file(self, filename):
        """Сериализация объекта в файл."""
        if not filename.endswith('.pkl'):
            raise OperationNotAllowedError("Расширение файла должно быть .pkl")

        with builtins.open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename):
        """Десериализация объекта из файла."""
        if not filename.endswith('.pkl'):
            raise OperationNotAllowedError("Расширение файла должно быть .pkl")

        with builtins.open(filename, 'rb') as f:
            return pickle.load(f)