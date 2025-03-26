"""
Модуль pharmacy26 реализует классы для управления аптекой:
- Medicine - класс для описания лекарств
- Pharmacy - класс для управления ассортиментом аптеки
"""

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
    """
    Класс для описания лекарства в аптеке.

    Атрибуты:
    - id: уникальный идентификатор лекарства (только для чтения)
    - name: название лекарства
    - price: цена за единицу (должна быть положительной)
    - quantity: количество на складе (должно быть неотрицательным)
    - expiry_date: срок годности в формате строки

    Методы:
    - sell(): продажа указанного количества лекарства
    - restock(): пополнение запасов лекарства
    - get_transactions(): получение истории операций
    """

    __next_id = 1

    def __init__(self, name="Неизвестно", price=0, quantity=0, expiry_date="2023-12-31"):
        """
        Инициализация лекарства.

        Args:
            name (str): Название лекарства
            price (float): Цена за единицу
            quantity (int): Количество на складе
            expiry_date (str): Срок годности

        Raises:
            InvalidMedicineError: Если цена или количество отрицательные
        """
        self.__id = Medicine.__next_id
        Medicine.__next_id += 1
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__expiry_date = expiry_date
        self.__transactions = []
        atexit.register(self._safe_close)

        if price < 0:
            raise InvalidMedicineError("цена", price)
        if quantity < 0:
            raise InvalidMedicineError("количество", quantity)

    @property
    def id(self):
        """Уникальный идентификатор лекарства (только для чтения)"""
        return self.__id

    @property
    def name(self):
        """Название лекарства"""
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise InvalidMedicineError("название", value)
        self.__name = value

    @property
    def price(self):
        """Цена за единицу (должна быть положительной)"""
        return self.__price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise InvalidMedicineError("цена", value)
        self.__price = value

    @property
    def quantity(self):
        """Количество на складе (должно быть неотрицательным)"""
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidMedicineError("количество", value)
        self.__quantity = value

    @property
    def expiry_date(self):
        """Срок годности в формате строки"""
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

    def __add__(self, amount):
        """
        Перегрузка оператора + для пополнения запасов

        Args:
            amount (int): Количество для пополнения

        Returns:
            Medicine: Возвращает self для цепочки операций

        Raises:
            InvalidMedicineError: Если количество отрицательное
        """
        self.restock(amount)
        return self

    def __sub__(self, amount):
        """
        Перегрузка оператора - для продажи лекарства

        Args:
            amount (int): Количество для продажи

        Returns:
            Medicine: Возвращает self для цепочки операций

        Raises:
            OperationNotAllowedError: Если недостаточно товара
            InvalidMedicineError: Если количество отрицательное
        """
        self.sell(amount)
        return self

    def __mul__(self, factor):
        """
        Перегрузка оператора * для изменения цены

        Args:
            factor (float): Множитель для цены

        Returns:
            Medicine: Новый объект с измененной ценой

        Raises:
            InvalidMedicineError: Если множитель отрицательный
        """
        if factor < 0:
            raise InvalidMedicineError("множитель цены", factor)
        new_medicine = Medicine(self.__name, self.__price * factor, self.__quantity, self.__expiry_date)
        return new_medicine

    def __truediv__(self, divisor):
        """
        Перегрузка оператора / для изменения цены

        Args:
            divisor (float): Делитель для цены

        Returns:
            Medicine: Новый объект с измененной ценой

        Raises:
            InvalidMedicineError: Если делитель отрицательный или ноль
        """
        if divisor <= 0:
            raise InvalidMedicineError("делитель цены", divisor)
        new_medicine = Medicine(self.__name, self.__price / divisor, self.__quantity, self.__expiry_date)
        return new_medicine

    def sell(self, amount=1):
        """
        Продажа указанного количества лекарства.

        Args:
            amount (int): Количество для продажи

        Returns:
            bool: True если продажа прошла успешно

        Raises:
            OperationNotAllowedError: Если недостаточно товара
            InvalidMedicineError: Если количество отрицательное
        """
        if amount <= 0:
            raise InvalidMedicineError("количество для продажи", amount)

        if self.__quantity < amount:
            raise OperationNotAllowedError(f"Недостаточно товара (доступно: {self.__quantity}, запрошено: {amount})")

        old_quantity = self.__quantity
        self.__quantity -= amount
        self.__log_transaction('Продажа', old_quantity, self.__quantity, amount)
        return True

    def restock(self, amount=1):
        """
        Пополнение запасов лекарства.

        Args:
            amount (int): Количество для пополнения

        Raises:
            InvalidMedicineError: Если количество отрицательное
        """
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
        """Возвращает копию списка транзакций"""
        return self.__transactions.copy()


class Pharmacy:
    """
    Класс для управления ассортиментом аптеки.

    Атрибуты:
    - name: название аптеки
    - medicines: список лекарств (только для чтения)

    Методы:
    - add_medicine(): добавление лекарства в ассортимент
    - save_to_file(): сохранение аптеки в файл
    - load_from_file(): загрузка аптеки из файла
    """

    def __init__(self, name="Аптека"):
        """
        Инициализация аптеки.

        Args:
            name (str): Название аптеки
        """
        self.__name = name
        self.__medicines = []
        self.__transactions = []
        atexit.register(self._safe_close)

    @property
    def name(self):
        """Название аптеки"""
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise InvalidMedicineError("название аптеки", value)
        self.__name = value

    @property
    def medicines(self):
        """Список лекарств (только для чтения)"""
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

    def __add__(self, medicine):
        """
        Перегрузка оператора + для добавления лекарства

        Args:
            medicine (Medicine): Лекарство для добавления

        Returns:
            Pharmacy: Возвращает self для цепочки операций

        Raises:
            InvalidMedicineError: Если передан не объект Medicine
        """
        self.add_medicine(medicine)
        return self

    def __sub__(self, medicine):
        """
        Перегрузка оператора - для удаления лекарства

        Args:
            medicine (Medicine): Лекарство для удаления

        Returns:
            Pharmacy: Возвращает self для цепочки операций
        """
        if medicine in self.__medicines:
            self.__medicines.remove(medicine)
            self.__log_transaction('Удаление лекарства', None, None, medicine.name)
        return self

    def add_medicine(self, medicine):
        """
        Добавление лекарства в ассортимент.

        Args:
            medicine (Medicine): Лекарство для добавления

        Returns:
            str: Сообщение о результате операции

        Raises:
            InvalidMedicineError: Если передан не объект Medicine
        """
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
        """Возвращает копию списка транзакций аптеки"""
        return self.__transactions.copy()

    def save_to_file(self, filename):
        """
        Сериализация объекта в файл.

        Args:
            filename (str): Имя файла (должно оканчиваться на .pkl)

        Raises:
            OperationNotAllowedError: Если расширение файла не .pkl
        """
        if not filename.endswith('.pkl'):
            raise OperationNotAllowedError("Расширение файла должно быть .pkl")

        with builtins.open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename):
        """
        Десериализация объекта из файла.

        Args:
            filename (str): Имя файла (должно оканчиваться на .pkl)

        Returns:
            Pharmacy: Загруженный объект аптеки

        Raises:
            OperationNotAllowedError: Если расширение файла не .pkl
        """
        if not filename.endswith('.pkl'):
            raise OperationNotAllowedError("Расширение файла должно быть .pkl")

        with builtins.open(filename, 'rb') as f:
            return pickle.load(f)