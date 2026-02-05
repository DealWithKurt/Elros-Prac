import unittest
import tempfile
import os
import json
from pathlib import Path

from utils import (
    add,
    sub,
    mul,
    div,
    is_prime,
    calculate_statistics,
    avg_grade,
    sort_by_age,
    best_students,
    unique_names,
    read_numbers_from_file,
    save_with_atomic_write,
    load_json_file,
    save_json_file
)


class TestMathUtils(unittest.TestCase):
    """Тесты для математических функций."""

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)
        self.assertEqual(sub(0, 5), -5)
        self.assertEqual(sub(10, 10), 0)

    def test_mul(self):
        self.assertEqual(mul(3, 4), 12)
        self.assertEqual(mul(-2, 3), -6)
        self.assertEqual(mul(0, 100), 0)

    def test_div(self):
        self.assertEqual(div(10, 2), 5)
        self.assertEqual(div(5, 2), 2.5)
        self.assertEqual(div(0, 5), 0)

        with self.assertRaises(ValueError):
            div(10, 0)

    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(13))

        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(15))

    def test_calculate_statistics(self):
        numbers = [1, 2, 3, 4, 5]
        stats = calculate_statistics(numbers)

        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 5)
        self.assertEqual(stats['average'], 3.0)

        empty_stats = calculate_statistics([])
        self.assertEqual(empty_stats['count'], 0)
        self.assertIsNone(empty_stats['min'])
        self.assertIsNone(empty_stats['max'])
        self.assertIsNone(empty_stats['average'])


class TestStudentUtils(unittest.TestCase):
    """Тесты для функций работы со студентами."""

    def setUp(self):
        self.students = [
            {"name": "Иван", "age": 20, "grades": [5, 4, 3]},
            {"name": "Мария", "age": 21, "grades": [5, 5, 5]},
            {"name": "Алексей", "age": 19, "grades": [3, 4, 4]},
            {"name": "Мария", "age": 22, "grades": [4, 4, 4]},
        ]

    def test_avg_grade(self):
        student = {"name": "Тест", "grades": [5, 4, 3]}
        self.assertAlmostEqual(avg_grade(student), 4.0)

        student2 = {"name": "Тест2", "grades": [5, 5, 5, 5]}
        self.assertAlmostEqual(avg_grade(student2), 5.0)

        with self.assertRaises(KeyError):
            avg_grade({"name": "Без оценок"})

        with self.assertRaises(ValueError):
            avg_grade({"name": "Пустые оценки", "grades": []})

    def test_sort_by_age(self):
        sorted_students = sort_by_age(self.students)
        ages = [s['age'] for s in sorted_students]
        self.assertEqual(ages, [19, 20, 21, 22])

        sorted_desc = sort_by_age(self.students, reverse=True)
        ages_desc = [s['age'] for s in sorted_desc]
        self.assertEqual(ages_desc, [22, 21, 20, 19])

    def test_best_students(self):
        best = best_students(self.students, top=2)
        self.assertEqual(len(best), 2)
        self.assertEqual(best[0]['name'], 'Мария')  # Средний 5.0
        self.assertEqual(best[1]['name'], 'Мария')  # Средний 4.0

        self.assertIn('avg_grade', best[0])
        self.assertAlmostEqual(best[0]['avg_grade'], 5.0)

    def test_unique_names(self):
        unique = unique_names(self.students)
        self.assertEqual(len(unique), 3)
        self.assertIn('Иван', unique)
        self.assertIn('Мария', unique)
        self.assertIn('Алексей', unique)


class TestFileUtils(unittest.TestCase):
    """Тесты для функций работы с файлами."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.txt"
        self.test_json = Path(self.temp_dir) / "test.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_read_numbers_from_file(self):
        content = "10\n20\n30\nabc\n\n40\n"
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(content)

        numbers = read_numbers_from_file(self.test_file)
        self.assertEqual(numbers, [10.0, 20.0, 30.0, 40.0])

        with self.assertRaises(FileNotFoundError):
            read_numbers_from_file("несуществующий_файл.txt")

    def test_save_with_atomic_write(self):
        content = "Тестовое содержание\nВторая строка"
        save_with_atomic_write(content, self.test_file)

        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        self.assertEqual(saved_content, content)

    def test_load_json_file(self):
        test_data = {"students": [{"name": "Иван", "age": 20}]}
        with open(self.test_json, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        loaded = load_json_file(self.test_json)
        self.assertEqual(loaded, test_data)

        with open(self.test_json, 'w', encoding='utf-8') as f:
            f.write("{невалидный json}")

        with self.assertRaises(json.JSONDecodeError):
            load_json_file(self.test_json)

    def test_save_json_file(self):
        test_data = [{"id": 1, "value": "test"}]
        save_json_file(test_data, self.test_json)

        self.assertTrue(os.path.exists(self.test_json))

        with open(self.test_json, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        self.assertEqual(loaded, test_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)