import pickle
from datetime import datetime
import builtins  # Импортируем модуль builtins для безопасного доступа к open


class Medicine:
    """Класс для описания лекарства в аптеке."""

    _next_id = 1

    def __init__(self, name="Неизвестно", price=0, quantity=0, expiry_date="2023-12-31"):
        self.id = Medicine._next_id
        Medicine._next_id += 1
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.transactions = []

    def __del__(self):
        try:
            with builtins.open('medicine_deleted.log', 'a') as f:
                f.write(f'{datetime.now()}: Удалено лекарство {self.name} (ID: {self.id})\n')
        except:
            pass  # Игнорируем ошибки при удалении

    def __str__(self):
        return (f"Лекарство #{self.id}: {self.name}, Цена: {self.price} руб., "
                f"Количество: {self.quantity}, Годен до: {self.expiry_date}")

    def sell(self, amount=1):
        if self.quantity >= amount:
            old_quantity = self.quantity
            self.quantity -= amount
            self._log_transaction('Продажа', old_quantity, self.quantity, amount)
            return True
        return False

    def restock(self, amount=1):
        old_quantity = self.quantity
        self.quantity += amount
        self._log_transaction('Пополнение', old_quantity, self.quantity, amount)

    def _log_transaction(self, operation, old_value, new_value, amount):
        transaction = {
            'datetime': datetime.now(),
            'operation': operation,
            'old_value': old_value,
            'new_value': new_value,
            'amount': amount
        }
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class Pharmacy:
    """Класс для управления ассортиментом аптеки."""

    def __init__(self, name="Аптека"):
        self.name = name
        self.medicines = []
        self.transactions = []

    def __del__(self):
        try:
            with builtins.open('pharmacy_deleted.log', 'a') as f:
                f.write(f'{datetime.now()}: Удалена аптека {self.name}\n')
        except:
            pass  # Игнорируем ошибки при удалении

    def __str__(self):
        return f"{self.name}. Лекарств в ассортименте: {len(self.medicines)}"

    def add_medicine(self, medicine):
        self.medicines.append(medicine)
        self._log_transaction('Добавление лекарства', None, None, medicine.name)
        return f"Добавлено: {medicine.name}"

    def _log_transaction(self, operation, old_value, new_value, details):
        transaction = {
            'datetime': datetime.now(),
            'operation': operation,
            'details': details
        }
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def save_to_file(self, filename):
        with builtins.open(filename, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename):
        with builtins.open(filename, 'rb') as f:
            return pickle.load(f)


if __name__ == '__main__':
    # Демонстрация работы
    print("--- Демонстрация работы классов ---")

    # Создаем лекарства
    aspirin = Medicine("Аспирин", 80, 50, "2025-05-30")
    paracetamol = Medicine("Парацетамол", 50, 100)

    # Работа с лекарствами
    aspirin.sell(10)
    aspirin.restock(20)
    paracetamol.sell(5)

    # Создаем аптеку и добавляем лекарства
    apteka = Pharmacy("Главная Аптека")
    apteka.add_medicine(aspirin)
    apteka.add_medicine(paracetamol)

    # Сохраняем аптеку в файл
    apteka.save_to_file('pharmacy_data.pkl')

    # Выводим информацию
    print(aspirin)
    print(apteka)

    # Выводим транзакции
    print("\nТранзакции по Аспирину:")
    for t in aspirin.get_transactions():
        print(f"{t['datetime']}: {t['operation']} {t['amount']} шт. Было: {t['old_value']}, Стало: {t['new_value']}")

    print("\nТранзакции аптеки:")
    for t in apteka.get_transactions():
        print(f"{t['datetime']}: {t['operation']} - {t['details']}")

    # Явно удаляем объекты до завершения программы
    del aspirin
    del paracetamol
    del apteka