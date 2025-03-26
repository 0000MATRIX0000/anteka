"""
Модуль test_pharmacy26 содержит тесты для проверки:
- Документации классов и методов
- Перегрузки операторов
- Корректности работы классов
"""

import unittest
import os
from datetime import datetime
from pharmacy26 import Medicine, Pharmacy, InvalidMedicineError, OperationNotAllowedError
import pickle


class TestPharmacy(unittest.TestCase):
    """Тесты для классов аптеки"""

    def setUp(self):
        """Подготовка тестовых данных"""
        Medicine._Medicine__next_id = 1
        self.test_medicine = Medicine("Ибупрофен", 120, 30)
        self.test_pharmacy = Pharmacy("Тестовая Аптека")

        # Очищаем логи перед тестами
        for filename in ['medicine_deleted.log', 'pharmacy_deleted.log']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_documentation(self):
        """Проверка наличия документации"""
        self.assertIsNotNone(Medicine.__doc__)
        self.assertIsNotNone(Medicine.__init__.__doc__)
        self.assertIsNotNone(Medicine.sell.__doc__)
        self.assertIsNotNone(Pharmacy.__doc__)
        self.assertIsNotNone(Pharmacy.add_medicine.__doc__)

    def test_medicine_operator_overloading(self):
        """Тестирование перегрузки операторов для Medicine"""
        # Оператор +
        self.test_medicine + 10
        self.assertEqual(self.test_medicine.quantity, 40)

        # Оператор -
        self.test_medicine - 5
        self.assertEqual(self.test_medicine.quantity, 35)

        # Оператор *
        new_med = self.test_medicine * 1.5
        self.assertEqual(new_med.price, 180)

        # Оператор /
        new_med = self.test_medicine / 2
        self.assertEqual(new_med.price, 60)

        # Проверка ошибок
        with self.assertRaises(InvalidMedicineError):
            self.test_medicine + (-5)

        with self.assertRaises(OperationNotAllowedError):
            self.test_medicine - 100

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine * (-1)

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine / 0

    def test_pharmacy_operator_overloading(self):
        """Тестирование перегрузки операторов для Pharmacy"""
        med1 = Medicine("Аспирин", 80, 50)
        med2 = Medicine("Парацетамол", 50, 100)

        # Оператор +
        self.test_pharmacy + med1
        self.assertEqual(len(self.test_pharmacy.medicines), 1)

        # Оператор -
        self.test_pharmacy - med1
        self.assertEqual(len(self.test_pharmacy.medicines), 0)

        # Цепочка операций
        self.test_pharmacy + med1 + med2
        self.assertEqual(len(self.test_pharmacy.medicines), 2)

    def test_medicine_creation(self):
        """Тестирование создания лекарства"""
        self.assertEqual(self.test_medicine.name, "Ибупрофен")
        self.assertEqual(self.test_medicine.price, 120)
        self.assertEqual(self.test_medicine.quantity, 30)

    def test_medicine_invalid_values(self):
        """Тестирование недопустимых значений лекарства"""
        with self.assertRaises(InvalidMedicineError):
            Medicine("Аспирин", -10, 50)

        with self.assertRaises(InvalidMedicineError):
            Medicine("Парацетамол", 50, -5)

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.price = -100

    def test_medicine_transactions(self):
        """Тестирование операций с лекарством"""
        self.test_medicine.sell(5)
        self.assertEqual(self.test_medicine.quantity, 25)

        with self.assertRaises(OperationNotAllowedError):
            self.test_medicine.sell(30)

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.sell(-1)

    def test_pharmacy_operations(self):
        """Тестирование операций аптеки"""
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.assertEqual(len(self.test_pharmacy.medicines), 1)

        with self.assertRaises(InvalidMedicineError):
            self.test_pharmacy.add_medicine("Не лекарство")

    def test_serialization(self):
        """Тестирование сериализации"""
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.test_pharmacy.save_to_file('test_pharmacy.pkl')

        loaded_pharmacy = Pharmacy.load_from_file('test_pharmacy.pkl')
        self.assertEqual(loaded_pharmacy.name, "Тестовая Аптека")

        with self.assertRaises(OperationNotAllowedError):
            self.test_pharmacy.save_to_file('test_pharmacy.txt')

    def tearDown(self):
        """Очистка после тестов"""
        for filename in ['test_pharmacy.pkl', 'medicine_deleted.log', 'pharmacy_deleted.log']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()