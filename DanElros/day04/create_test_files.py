import json
import random
from pathlib import Path


def create_numbers_file():
    """Создает файл с 20-40 случайными числами"""
    numbers = [random.randint(1, 100) for _ in range(random.randint(20, 40))]

    with open('io_tasks/numbers.txt', 'w', encoding='utf-8') as f:
        for num in numbers:
            f.write(f"{num}\n")

    with open('io_tasks/numbers.txt', 'a', encoding='utf-8') as f:
        f.write("\n")
        f.write("abc\n")
        f.write("123abc\n")
        f.write("   \n")

    print(f"Создан файл numbers.txt с {len(numbers)} числами и тестовыми строками")


def create_students_json():
    """Создает JSON файл с данными студентов из Дня 3"""
    students = [
        {"name": "Иван", "age": 18, "grades": [5, 4, 3, 5]},
        {"name": "Мария", "age": 19, "grades": [5, 5, 5, 4]},
        {"name": "Алексей", "age": 20, "grades": [3, 4, 4, 3]},
        {"name": "Екатерина", "age": 18, "grades": [4, 5, 5, 5]},
        {"name": "Дмитрий", "age": 21, "grades": [3, 3, 4, 4]},
        {"name": "Анна", "age": 19, "grades": [5, 4, 5, 4]},
        {"name": "Сергей", "age": 22, "grades": [4, 4, 3, 4]},
        {"name": "Ольга", "age": 18, "grades": [5, 5, 4, 5]},
        {"name": "Павел", "age": 20, "grades": [4, 3, 4, 3]},
        {"name": "Иван", "age": 19, "grades": [4, 4, 4, 4]}
    ]

    with open('io_tasks/students.json', 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

    print("Создан файл students.json с 10 студентами")


def main():
    Path('io_tasks').mkdir(exist_ok=True)

    create_numbers_file()
    create_students_json()
    print("\nТестовые файлы созданы в папке io_tasks/")


if __name__ == "__main__":
    main()