"""
Модуль pharmacy27 реализует систему управления аптекой с:
- Классами для лекарств и аптек
- Ассоциацией с классом поставщика
- Декораторами для логирования
"""

import time
from datetime import datetime
from functools import wraps

# Декораторы
def timing_decorator(func):
    """Декоратор для измерения времени выполнения метода"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Метод {func.__name__} выполнен за {end_time - start_time:.4f} сек")
        return result
    return wrapper

def call_counter_decorator(func):
    """Декоратор для подсчета вызовов метода"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_call_counts'):
            self._call_counts = {}
        self._call_counts[func.__name__] = self._call_counts.get(func.__name__, 0) + 1
        print(f"Метод {func.__name__} вызван {self._call_counts[func.__name__]} раз")
        return func(self, *args, **kwargs)
    return wrapper

class Supplier:
    """
    Класс поставщика лекарств.
    Ассоциируется с классом Pharmacy через отношение использования.
    """
    def __init__(self, name, contact_phone):
        self.name = name
        self.contact_phone = contact_phone
        self.supplied_medicines = []
        self._call_counts = {}

    def __str__(self):
        return f"Поставщик: {self.name}, тел: {self.contact_phone}"

    @call_counter_decorator
    def add_supplied_medicine(self, medicine_name):
        """Добавляет лекарство в список поставляемых"""
        self.supplied_medicines.append(medicine_name)
        return f"{medicine_name} добавлен к списку поставляемых"

    def get_call_count(self, method_name):
        """Возвращает количество вызовов указанного метода"""
        return self._call_counts.get(method_name, 0)

class Medicine:
    """Класс для описания лекарства в аптеке."""

    def __init__(self, name, price, quantity, expiry_date):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.supplier = None  # Ассоциация с поставщиком

    def __str__(self):
        supplier_info = f", Поставщик: {self.supplier.name}" if self.supplier else ""
        return (f"Лекарство: {self.name}, Цена: {self.price} руб., "
                f"Количество: {self.quantity}, Годен до: {self.expiry_date}"
                f"{supplier_info}")

    @timing_decorator
    def set_supplier(self, supplier):
        """Устанавливает поставщика для лекарства"""
        if not isinstance(supplier, Supplier):
            raise TypeError("Должен быть объект класса Supplier")
        self.supplier = supplier

class Pharmacy:
    """Класс для управления ассортиментом аптеки."""

    def __init__(self, name):
        self.name = name
        self.medicines = []
        self.suppliers = []
        self._call_counts = {}  # Для хранения счетчиков вызовов

    def __str__(self):
        return f"Аптека '{self.name}'. Лекарств: {len(self.medicines)}, Поставщиков: {len(self.suppliers)}"

    @call_counter_decorator
    def add_medicine(self, medicine):
        """Добавляет лекарство в ассортимент"""
        if not isinstance(medicine, Medicine):
            raise TypeError("Должен быть объект класса Medicine")
        self.medicines.append(medicine)
        return f"Лекарство {medicine.name} добавлено в ассортимент"

    @timing_decorator
    @call_counter_decorator
    def add_supplier(self, supplier):
        """Добавляет поставщика"""
        if not isinstance(supplier, Supplier):
            raise TypeError("Должен быть объект класса Supplier")
        self.suppliers.append(supplier)
        return f"Поставщик {supplier.name} добавлен"

    @timing_decorator
    def restock_from_supplier(self, supplier, medicine_name, quantity):
        """
        Пополняет запасы от указанного поставщика.
        Возвращает строку с информацией о пополнении.
        """
        if supplier not in self.suppliers:
            raise ValueError("Этот поставщик не сотрудничает с аптекой")

        if medicine_name not in supplier.supplied_medicines:
            raise ValueError("Этот поставщик не поставляет указанное лекарство")

        # Ищем лекарство в ассортименте
        for med in self.medicines:
            if med.name == medicine_name:
                med.quantity += quantity
                if not med.supplier:
                    med.set_supplier(supplier)
                return f"Запас {medicine_name} пополнен на {quantity} единиц"

        # Если лекарства нет в ассортименте
        new_med = Medicine(medicine_name, 0, quantity, "2025-12-31")
        new_med.set_supplier(supplier)
        self.add_medicine(new_med)
        return f"Запас {medicine_name} пополнен на {quantity} единиц (новое лекарство)"

    def get_call_count(self, method_name):
        """Возвращает количество вызовов указанного метода"""
        return self._call_counts.get(method_name, 0)

if __name__ == '__main__':
    # Демонстрация работы
    print("=== Демонстрация работы системы ===")

    # Создаем аптеку
    apteka = Pharmacy("Главная Аптека")
    print(apteka)

    # Создаем поставщиков
    supplier1 = Supplier("Фармакор", "88002000600")
    supplier2 = Supplier("Медпоставка", "88003000700")

    # Добавляем поставщиков
    apteka.add_supplier(supplier1)
    apteka.add_supplier(supplier2)
    print(apteka)

    # Добавляем лекарства к поставщикам
    supplier1.add_supplied_medicine("Аспирин")
    supplier1.add_supplied_medicine("Ибупрофен")
    supplier2.add_supplied_medicine("Парацетамол")

    # Пополняем запасы от поставщиков
    print("\nПополнение запасов:")
    print(apteka.restock_from_supplier(supplier1, "Аспирин", 100))
    print(apteka.restock_from_supplier(supplier1, "Ибупрофен", 50))
    print(apteka.restock_from_supplier(supplier2, "Парацетамол", 75))

    # Выводим информацию о лекарствах
    print("\nАссортимент аптеки:")
    for med in apteka.medicines:
        print(med)

    # Проверяем счетчики вызовов
    print("\nСтатистика вызовов:")
    print(f"add_supplier вызван {apteka.get_call_count('add_supplier')} раз")
    print(f"add_medicine вызван {apteka.get_call_count('add_medicine')} раз")
    print(f"add_supplied_medicine вызван {supplier1.get_call_count('add_supplied_medicine')} раз")