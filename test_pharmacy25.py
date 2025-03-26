import unittest
import os
from datetime import datetime
from pharmacy25 import Medicine, Pharmacy, InvalidMedicineError, OperationNotAllowedError
import pickle


class TestPharmacy(unittest.TestCase):
    def setUp(self):
        Medicine._Medicine__next_id = 1  # Доступ к приватному атрибуту
        self.test_medicine = Medicine("Ибупрофен", 120, 30)
        self.test_pharmacy = Pharmacy("Тестовая Аптека")

        # Очищаем логи перед тестами
        for filename in ['medicine_deleted.log', 'pharmacy_deleted.log']:
            if os.path.exists(filename):
                os.remove(filename)

    def test_medicine_creation(self):
        self.assertEqual(self.test_medicine.name, "Ибупрофен")
        self.assertEqual(self.test_medicine.price, 120)
        self.assertEqual(self.test_medicine.quantity, 30)

    def test_medicine_invalid_values(self):
        with self.assertRaises(InvalidMedicineError):
            Medicine("Аспирин", -10, 50)

        with self.assertRaises(InvalidMedicineError):
            Medicine("Парацетамол", 50, -5)

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.price = -100

    def test_medicine_transactions(self):
        self.test_medicine.sell(5)
        self.assertEqual(self.test_medicine.quantity, 25)

        with self.assertRaises(OperationNotAllowedError):
            self.test_medicine.sell(30)

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.sell(-1)

    def test_pharmacy_operations(self):
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.assertEqual(len(self.test_pharmacy.medicines), 1)

        with self.assertRaises(InvalidMedicineError):
            self.test_pharmacy.add_medicine("Не лекарство")

    def test_serialization(self):
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.test_pharmacy.save_to_file('test_pharmacy.pkl')

        loaded_pharmacy = Pharmacy.load_from_file('test_pharmacy.pkl')
        self.assertEqual(loaded_pharmacy.name, "Тестовая Аптека")

        with self.assertRaises(OperationNotAllowedError):
            self.test_pharmacy.save_to_file('test_pharmacy.txt')

    def test_properties(self):
        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.price = "сто"

        with self.assertRaises(InvalidMedicineError):
            self.test_medicine.quantity = 5.5

    def tearDown(self):
        for filename in ['test_pharmacy.pkl', 'medicine_deleted.log', 'pharmacy_deleted.log']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()