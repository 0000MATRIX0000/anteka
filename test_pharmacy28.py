"""
Модуль test_pharmacy28 содержит тесты для:
- Контейнеров лекарств и поставщиков
- Итераторов
- Функциональности управления
"""

import unittest
import os
from pharmacy28 import Medicine, Supplier, MedicineDatabase, SupplierDatabase


class TestPharmacySystem(unittest.TestCase):
    """Тесты для системы управления аптекой"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Очищаем файлы перед тестами
        for filename in ['medicines.pkl', 'suppliers.pkl']:
            if os.path.exists(filename):
                os.remove(filename)

        self.med_db = MedicineDatabase()
        self.sup_db = SupplierDatabase()

        # Тестовые данные
        self.medicine = Medicine("Аспирин", 50.0, 100, "2025-12-31")
        self.supplier = Supplier("Фармакор", "88002000600")

    def test_medicine_container(self):
        """Тестирование контейнера для лекарств"""
        # Добавление
        self.med_db.add(self.medicine)
        self.assertEqual(len(self.med_db), 1)

        # Получение
        med = self.med_db.get("Аспирин")
        self.assertEqual(med.name, "Аспирин")

        # Итерация
        for med in self.med_db:
            self.assertEqual(med.name, "Аспирин")

        # Удаление
        self.assertTrue(self.med_db.remove("Аспирин"))
        self.assertEqual(len(self.med_db), 0)

    def test_supplier_container(self):
        """Тестирование контейнера для поставщиков"""
        # Добавление
        self.sup_db.add(self.supplier)
        self.assertEqual(len(self.sup_db), 1)

        # Получение
        sup = self.sup_db.get("Фармакор")
        self.assertEqual(sup.name, "Фармакор")

        # Итерация
        for sup in self.sup_db:
            self.assertEqual(sup.name, "Фармакор")

        # Удаление
        self.assertTrue(self.sup_db.remove("Фармакор"))
        self.assertEqual(len(self.sup_db), 0)

    def test_medicine_supplier_association(self):
        """Тестирование связи лекарства и поставщика"""
        self.med_db.add(self.medicine)
        self.sup_db.add(self.supplier)

        # Назначаем поставщика
        self.medicine.supplier = self.supplier
        self.supplier.add_medicine(self.medicine.name)

        # Проверяем связь
        self.assertEqual(self.medicine.supplier.name, "Фармакор")
        self.assertIn("Аспирин", self.supplier.supplied_medicines)

    def test_persistence(self):
        """Тестирование сохранения и загрузки данных"""
        # Добавляем данные
        self.med_db.add(self.medicine)
        self.sup_db.add(self.supplier)

        # Создаем новые контейнеры (должны загрузить данные)
        new_med_db = MedicineDatabase()
        new_sup_db = SupplierDatabase()

        # Проверяем загруженные данные
        self.assertEqual(len(new_med_db), 1)
        self.assertEqual(len(new_sup_db), 1)
        self.assertEqual(new_med_db.get("Аспирин").name, "Аспирин")
        self.assertEqual(new_sup_db.get("Фармакор").name, "Фармакор")

    def tearDown(self):
        """Очистка после тестов"""
        for filename in ['medicines.pkl', 'suppliers.pkl']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()