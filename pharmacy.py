class Medicine:
    """Класс для описания лекарства в аптеке."""

    # Классовая переменная для генерации ID
    _next_id = 1

    def __init__(self, name="Неизвестно", price=0, quantity=0, expiry_date="2023-12-31"):
        self.id = Medicine._next_id
        Medicine._next_id += 1
        self.name = name
        self.price = price
        self.quantity = quantity
        self.expiry_date = expiry_date

    def __str__(self):
        return (f"Лекарство #{self.id}: {self.name}, Цена: {self.price} руб., "
                f"Количество: {self.quantity}, Годен до: {self.expiry_date}")

    def sell(self, amount=1):
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False


class Pharmacy:
    """Класс для управления ассортиментом аптеки."""

    def __init__(self, name="Аптека"):
        self.name = name
        self.medicines = []

    def __str__(self):
        return f"{self.name}. Лекарств в ассортименте: {len(self.medicines)}"

    def add_medicine(self, medicine):
        self.medicines.append(medicine)
        return f"Добавлено: {medicine.name}"


if __name__ == '__main__':
    # Демонстрация работы
    print("--- Демонстрация классов ---")
    Medicine._next_id = 1  # Сбрасываем счетчик для демонстрации
    aspirin = Medicine("Аспирин", 80, 50, "2025-05-30")
    print(aspirin)

    apteka = Pharmacy("Главная Аптека")
    apteka.add_medicine(aspirin)
    print(apteka)