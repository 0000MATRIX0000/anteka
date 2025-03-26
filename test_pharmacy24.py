import unittest
import os
from datetime import datetime
from pharmacy24 import Medicine, Pharmacy
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

    # ... другие тесты без изменений ...

    def test_destructor_logs(self):
        """Тестирование работы деструкторов с принудительной записью логов."""
        # Создаем временные объекты
        med = Medicine("Тестовое лекарство")
        pharm = Pharmacy("Тестовая аптека для деструктора")

        # Явно вызываем деструкторы
        med._safe_close()
        pharm._safe_close()

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
        for filename in ['test_pharmacy.pkl', 'medicine_deleted.log', 'pharmacy_deleted.log']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()