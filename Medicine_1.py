class Medicine:
    """Класс для описания лекарства в аптеке."""

    def __init__(self, name, price, quantity, expiry_date):
        self.name = name  # Название лекарства
        self.price = price  # Цена
        self.quantity = quantity  # Количество на складе
        self.expiry_date = expiry_date  # Срок годности (строка в формате 'YYYY-MM-DD')

    def get_info(self):
        """Возвращает информацию о лекарстве."""
        return f"{self.name}, Цена: {self.price} руб., Количество: {self.quantity}, Годен до: {self.expiry_date}"

    def sell(self, amount):
        """Продажа указанного количества лекарства."""
        if self.quantity >= amount:
            self.quantity -= amount
            return f"Продано {amount} шт. {self.name}. Остаток: {self.quantity}"
        else:
            return f"Недостаточно {self.name} на складе (доступно: {self.quantity})"

    def restock(self, amount):
        """Пополнение запасов лекарства."""
        self.quantity += amount
        return f"Добавлено {amount} шт. {self.name}. Теперь: {self.quantity}"


class Pharmacy:
    """Класс для управления ассортиментом аптеки."""

    def __init__(self, name):
        self.name = name  # Название аптеки
        self.medicines = []  # Список лекарств

    def add_medicine(self, medicine):
        """Добавляет лекарство в ассортимент."""
        self.medicines.append(medicine)
        return f"Лекарство {medicine.name} добавлено в {self.name}"

    def find_medicine(self, name):
        """Ищет лекарство по названию."""
        for med in self.medicines:
            if med.name.lower() == name.lower():
                return med
        return None

    def sell_medicine(self, name, amount):
        """Продает лекарство, если оно есть в наличии."""
        medicine = self.find_medicine(name)
        if medicine:
            return medicine.sell(amount)
        else:
            return f"Лекарство {name} не найдено."


if __name__ == '__main__':
    # Тестирование классов
    print("--- Тест класса Medicine ---")
    aspirin = Medicine("Аспирин", 50, 100, "2025-12-31")
    print(aspirin.get_info())
    print(aspirin.sell(10))
    print(aspirin.restock(20))

    print("\n--- Тест класса Pharmacy ---")
    apteka = Pharmacy("Аптека №1")
    apteka.add_medicine(aspirin)
    apteka.add_medicine(Medicine("Ибупрофен", 80, 50, "2024-10-15"))

    print("\nПоиск лекарств:")
    print(apteka.find_medicine("Аспирин").get_info() if apteka.find_medicine("Аспирин") else "Не найдено")

    print("\nПопытка продажи:")
    print(apteka.sell_medicine("Ибупрофен", 10))
    print(apteka.sell_medicine("Парацетамол", 5))  # Несуществующее