import unittest
import os
from datetime import datetime
from pharmacy23 import Medicine, Pharmacy
import pickle


class TestPharmacy(unittest.TestCase):
    def setUp(self):
        Medicine._next_id = 1
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

    def test_medicine_transactions(self):
        # Проверяем продажу
        self.test_medicine.sell(5)
        self.assertEqual(self.test_medicine.quantity, 25)
        transactions = self.test_medicine.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['operation'], 'Продажа')

        # Проверяем пополнение
        self.test_medicine.restock(10)
        self.assertEqual(self.test_medicine.quantity, 35)
        self.assertEqual(len(self.test_medicine.get_transactions()), 2)

    def test_pharmacy_operations(self):
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.assertEqual(len(self.test_pharmacy.medicines), 1)
        self.assertEqual(self.test_pharmacy.medicines[0].name, "Ибупрофен")

        # Проверяем транзакции аптеки
        transactions = self.test_pharmacy.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['operation'], 'Добавление лекарства')

    def test_serialization(self):
        # Сохраняем аптеку
        self.test_pharmacy.add_medicine(self.test_medicine)
        self.test_pharmacy.save_to_file('test_pharmacy.pkl')

        # Загружаем аптеку
        loaded_pharmacy = Pharmacy.load_from_file('test_pharmacy.pkl')

        # Проверяем загруженные данные
        self.assertEqual(loaded_pharmacy.name, "Тестовая Аптека")
        self.assertEqual(len(loaded_pharmacy.medicines), 1)
        self.assertEqual(loaded_pharmacy.medicines[0].name, "Ибупрофен")

    def test_destructor_logs(self):
        # Создаем и сразу удаляем объекты
        med = Medicine("Тестовое лекарство")
        pharm = Pharmacy("Тестовая аптека для деструктора")
        del med
        del pharm

        # Проверяем логи деструкторов
        self.assertTrue(os.path.exists('medicine_deleted.log'))
        with open('medicine_deleted.log', 'r') as f:
            medicine_log = f.read()
        self.assertIn("Тестовое лекарство", medicine_log)

        self.assertTrue(os.path.exists('pharmacy_deleted.log'))
        with open('pharmacy_deleted.log', 'r') as f:
            pharmacy_log = f.read()
        self.assertIn("Тестовая аптека для деструктора", pharmacy_log)

    def tearDown(self):
        # Удаляем временные файлы после тестов
        if os.path.exists('test_pharmacy.pkl'):
            os.remove('test_pharmacy.pkl')


if __name__ == '__main__':
    unittest.main()