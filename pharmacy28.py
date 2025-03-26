"""
Модуль pharmacy28 реализует систему управления аптекой с:
- Классами для лекарств, поставщиков и аптек
- Контейнером для хранения данных
- Итераторами для обхода коллекций
- Консольным интерфейсом
"""

import pickle
from datetime import datetime
from functools import wraps


class MedicineDatabase:
    """Класс-контейнер для хранения лекарств"""

    def __init__(self):
        self.filename = 'medicines.pkl'
        self.medicines = {}
        try:
            self.load()
        except:
            self.save()

    def __iter__(self):
        """Итератор по всем лекарствам"""
        for med in self.medicines.values():
            yield med

    def __len__(self):
        return len(self.medicines)

    def add(self, medicine):
        """Добавление лекарства в базу"""
        if not isinstance(medicine, Medicine):
            raise TypeError("Должен быть объект класса Medicine")
        self.medicines[medicine.name] = medicine
        self.save()

    def get(self, name):
        """Получение лекарства по имени"""
        return self.medicines.get(name)

    def remove(self, name):
        """Удаление лекарства"""
        if name in self.medicines:
            del self.medicines[name]
            self.save()
            return True
        return False

    def save(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.medicines, f)

    def load(self):
        """Загрузка данных из файла"""
        with open(self.filename, 'rb') as f:
            self.medicines = pickle.load(f)


class SupplierDatabase:
    """Класс-контейнер для хранения поставщиков"""

    def __init__(self):
        self.filename = 'suppliers.pkl'
        self.suppliers = {}
        try:
            self.load()
        except:
            self.save()

    def __iter__(self):
        """Итератор по всем поставщикам"""
        for supplier in self.suppliers.values():
            yield supplier

    def __len__(self):
        return len(self.suppliers)

    def add(self, supplier):
        """Добавление поставщика в базу"""
        if not isinstance(supplier, Supplier):
            raise TypeError("Должен быть объект класса Supplier")
        self.suppliers[supplier.name] = supplier
        self.save()

    def get(self, name):
        """Получение поставщика по имени"""
        return self.suppliers.get(name)

    def remove(self, name):
        """Удаление поставщика"""
        if name in self.suppliers:
            del self.suppliers[name]
            self.save()
            return True
        return False

    def save(self):
        """Сохранение данных в файл"""
        with open(self.filename, 'wb') as f:
            pickle.dump(self.suppliers, f)

    def load(self):
        """Загрузка данных из файла"""
        with open(self.filename, 'rb') as f:
            self.suppliers = pickle.load(f)


class Medicine:
    """Класс для описания лекарства"""

    def __init__(self, name, price, quantity, expiry_date):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.supplier = None

    def __str__(self):
        supplier_info = f", Поставщик: {self.supplier.name}" if self.supplier else ""
        return (f"Лекарство: {self.name}, Цена: {self.price} руб., "
                f"Количество: {self.quantity}, Годен до: {self.expiry_date}"
                f"{supplier_info}")


class Supplier:
    """Класс для описания поставщика"""

    def __init__(self, name, contact_phone):
        self.name = name
        self.contact_phone = contact_phone
        self.supplied_medicines = []

    def __str__(self):
        return f"Поставщик: {self.name}, тел: {self.contact_phone}"

    def add_medicine(self, medicine_name):
        """Добавление лекарства в список поставляемых"""
        self.supplied_medicines.append(medicine_name)
        return f"{medicine_name} добавлен к списку поставляемых"


class PharmacyManager:
    """Класс для управления аптекой с консольным интерфейсом"""

    def __init__(self):
        self.med_db = MedicineDatabase()
        self.sup_db = SupplierDatabase()

    def print_all_medicines(self):
        """Вывод всех лекарств"""
        print("\nСписок лекарств:")
        for med in self.med_db:
            print(med)

    def print_all_suppliers(self):
        """Вывод всех поставщиков"""
        print("\nСписок поставщиков:")
        for sup in self.sup_db:
            print(sup)

    def add_medicine(self):
        """Добавление нового лекарства"""
        print("\nДобавление лекарства:")
        name = input("Название: ")
        price = float(input("Цена: "))
        quantity = int(input("Количество: "))
        expiry_date = input("Срок годности (ГГГГ-ММ-ДД): ")

        med = Medicine(name, price, quantity, expiry_date)
        self.med_db.add(med)
        print(f"Лекарство {name} добавлено")

    def add_supplier(self):
        """Добавление нового поставщика"""
        print("\nДобавление поставщика:")
        name = input("Название компании: ")
        phone = input("Контактный телефон: ")

        sup = Supplier(name, phone)
        self.sup_db.add(sup)
        print(f"Поставщик {name} добавлен")

    def assign_supplier(self):
        """Назначение поставщика лекарству"""
        print("\nНазначение поставщика:")
        med_name = input("Название лекарства: ")
        sup_name = input("Название поставщика: ")

        med = self.med_db.get(med_name)
        sup = self.sup_db.get(sup_name)

        if not med:
            print("Лекарство не найдено")
            return
        if not sup:
            print("Поставщик не найден")
            return

        med.supplier = sup
        sup.add_medicine(med_name)
        self.med_db.save()
        self.sup_db.save()
        print(f"Поставщик {sup_name} назначен для {med_name}")

    def run(self):
        """Запуск консольного интерфейса"""
        choices = {
            '1': self.print_all_medicines,
            '2': self.print_all_suppliers,
            '3': self.add_medicine,
            '4': self.add_supplier,
            '5': self.assign_supplier,
            '6': lambda: print("Выход из программы")
        }

        while True:
            print("\nМеню управления аптекой:")
            print("1. Показать все лекарства")
            print("2. Показать всех поставщиков")
            print("3. Добавить лекарство")
            print("4. Добавить поставщика")
            print("5. Назначить поставщика лекарству")
            print("6. Выход")

            choice = input("Выберите действие: ")
            if choice == '6':
                break
            if choice in choices:
                choices[choice]()
            else:
                print("Неверный выбор, попробуйте снова")


if __name__ == '__main__':
    PharmacyManager().run()