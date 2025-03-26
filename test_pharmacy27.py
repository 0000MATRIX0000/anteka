"""
Модуль test_pharmacy27 содержит тесты для:
- Проверки ассоциации классов
- Работы декораторов
- Корректности взаимодействия объектов
"""

import unittest
from pharmacy27 import Pharmacy, Medicine, Supplier

class TestPharmacySystem(unittest.TestCase):
    """Тесты для системы управления аптекой"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.pharmacy = Pharmacy("Тестовая Аптека")
        self.supplier = Supplier("Тестовый Поставщик", "88001000101")
        self.medicine = Medicine("Тестовое Лекарство", 100, 10, "2025-01-01")

    def test_association(self):
        """Тестирование ассоциации между классами"""
        # Добавляем поставщика в аптеку
        self.pharmacy.add_supplier(self.supplier)
        self.assertEqual(len(self.pharmacy.suppliers), 1)

        # Добавляем лекарство к поставщику
        self.supplier.add_supplied_medicine("Тестовое Лекарство")
        self.assertIn("Тестовое Лекарство", self.supplier.supplied_medicines)

        # Устанавливаем поставщика для лекарства
        self.medicine.set_supplier(self.supplier)
        self.assertEqual(self.medicine.supplier, self.supplier)

        # Проверяем строковое представление с поставщиком
        self.assertIn(self.supplier.name, str(self.medicine))

    def test_restock(self):
        """Тестирование пополнения запасов"""
        self.pharmacy.add_supplier(self.supplier)
        self.supplier.add_supplied_medicine("Тестовое Лекарство")

        # Первое пополнение - лекарство будет добавлено как новое
        result = self.pharmacy.restock_from_supplier(
            self.supplier, "Тестовое Лекарство", 50
        )
        self.assertIn("пополнен на 50", result)
        self.assertIn("новое лекарство", result)
        self.assertEqual(len(self.pharmacy.medicines), 1)
        self.assertEqual(self.pharmacy.medicines[0].quantity, 50)

        # Второе пополнение - лекарство уже есть
        result = self.pharmacy.restock_from_supplier(
            self.supplier, "Тестовое Лекарство", 30
        )
        self.assertIn("пополнен на 30", result)
        self.assertNotIn("новое лекарство", result)
        self.assertEqual(len(self.pharmacy.medicines), 1)
        self.assertEqual(self.pharmacy.medicines[0].quantity, 80)

    def test_decorators(self):
        """Тестирование работы декораторов"""
        # Проверяем счетчик вызовов для add_supplied_medicine
        initial_count = self.supplier.get_call_count('add_supplied_medicine')
        self.supplier.add_supplied_medicine("Лекарство 1")
        self.assertEqual(self.supplier.get_call_count('add_supplied_medicine'), initial_count + 1)

        # Проверяем счетчик вызовов для add_supplier
        initial_count = self.pharmacy.get_call_count('add_supplier')
        self.pharmacy.add_supplier(self.supplier)
        self.assertEqual(self.pharmacy.get_call_count('add_supplier'), initial_count + 1)

    def test_error_cases(self):
        """Тестирование обработки ошибок"""
        # Попытка добавить неверный тип
        with self.assertRaises(TypeError):
            self.pharmacy.add_supplier("Не поставщик")

        with self.assertRaises(TypeError):
            self.pharmacy.add_medicine("Не лекарство")

        with self.assertRaises(TypeError):
            self.medicine.set_supplier("Не поставщик")

        # Попытка пополнить от неизвестного поставщика
        bad_supplier = Supplier("Плохой Поставщик", "88001000102")
        with self.assertRaises(ValueError):
            self.pharmacy.restock_from_supplier(bad_supplier, "Лекарство", 10)

    def test_call_counters(self):
        """Тестирование счетчиков вызовов методов"""
        # Проверяем начальные значения
        self.assertEqual(self.pharmacy.get_call_count('add_supplier'), 0)
        self.assertEqual(self.pharmacy.get_call_count('add_medicine'), 0)
        self.assertEqual(self.supplier.get_call_count('add_supplied_medicine'), 0)

        # Вызываем методы и проверяем счетчики
        self.pharmacy.add_supplier(self.supplier)
        self.assertEqual(self.pharmacy.get_call_count('add_supplier'), 1)

        self.pharmacy.add_medicine(self.medicine)
        self.assertEqual(self.pharmacy.get_call_count('add_medicine'), 1)

        self.supplier.add_supplied_medicine("Лекарство")
        self.assertEqual(self.supplier.get_call_count('add_supplied_medicine'), 1)

if __name__ == '__main__':
    unittest.main()