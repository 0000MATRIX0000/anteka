import unittest
from pharmacy import Medicine, Pharmacy


class TestPharmacy(unittest.TestCase):
    def setUp(self):
        # Сбрасываем счетчик перед каждым тестом
        Medicine._next_id = 1

        self.pharmacy = Pharmacy("Тестовая Аптека")
        self.medicine1 = Medicine("Парацетамол", 50, 100)
        self.medicine2 = Medicine(price=150, quantity=50)

    def test_medicine_default_values(self):
        self.assertEqual(self.medicine2.name, "Неизвестно")
        self.assertEqual(self.medicine2.price, 150)

    def test_medicine_id_generation(self):
        self.assertEqual(self.medicine1.id, 1)
        self.assertEqual(self.medicine2.id, 2)

        medicine3 = Medicine("Аспирин")
        self.assertEqual(medicine3.id, 3)

    def test_medicine_str(self):
        expected_str = "Лекарство #1: Парацетамол, Цена: 50 руб., Количество: 100, Годен до: 2023-12-31"
        self.assertEqual(str(self.medicine1), expected_str)

    def test_pharmacy_add_medicine(self):
        result = self.pharmacy.add_medicine(self.medicine1)
        self.assertEqual(result, "Добавлено: Парацетамол")
        self.assertEqual(len(self.pharmacy.medicines), 1)

    @classmethod
    def tearDownClass(cls):
        # Восстанавливаем исходное состояние после всех тестов
        Medicine._next_id = 1


if __name__ == '__main__':
    unittest.main()