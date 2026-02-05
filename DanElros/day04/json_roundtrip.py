import json
import os
from pathlib import Path


def load_students(filename):
    """
    Загружает данные студентов из JSON файла.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка: невалидный JSON в файле {filename}: {e}")
        return []
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def save_students(data, filename):
    """
    Сохраняет данные студентов в JSON файл.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Данные успешно сохранены в {filename}")
        return True
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False


def add_new_student(students):
    """
    Добавляет нового студента к списку.
    Возвращает обновленный список.
    """
    new_student = {
        "name": "Артем",
        "age": 20,
        "grades": [5, 4, 5, 5, 4]
    }

    updated_students = students.copy()
    updated_students.append(new_student)

    print("Добавлен новый студент:")
    print(f"  Имя: {new_student['name']}")
    print(f"  Возраст: {new_student['age']}")
    print(f"  Оценки: {new_student['grades']}")

    return updated_students


def verify_files_different(original_file, updated_file):
    """
    Проверяет, что оригинальный и обновленный файлы разные.
    """
    try:
        with open(original_file, 'r', encoding='utf-8') as f1:
            with open(updated_file, 'r', encoding='utf-8') as f2:
                original_content = f1.read()
                updated_content = f2.read()

                if original_content == updated_content:
                    print("Внимание: файлы идентичны! Проверьте логику программы.")
                    return False
                else:
                    print("Проверка пройдена: файлы разные")
                    return True
    except IOError as e:
        print(f"Ошибка при проверке файлов: {e}")
        return False


def main():
    original_file = 'io_tasks/students.json'
    updated_file = 'io_tasks/students_updated.json'

    print("Загрузка данных студентов...")
    students = load_students(original_file)

    if not students:
        print("Не удалось загрузить данные. Проверьте файл students.json")
        return

    print(f"Загружено {len(students)} студентов")

    original_size = os.path.getsize(original_file)
    print(f"Размер исходного файла: {original_size} байт")

    updated_students = add_new_student(students)

    if save_students(updated_students, updated_file):
        current_original_size = os.path.getsize(original_file)
        if current_original_size == original_size:
            print("Проверка: исходный файл students.json не изменен")
        else:
            print("Внимание: исходный файл был изменен!")

        verify_files_different(original_file, updated_file)

        updated_size = os.path.getsize(updated_file)
        print(f"Размер нового файла: {updated_size} байт")
        print(f"Количество студентов в новом файле: {len(updated_students)}")

        try:
            with open(updated_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            print("Проверка: students_updated.json содержит валидный JSON")
        except json.JSONDecodeError:
            print("Ошибка: students_updated.json содержит невалидный JSON")


if __name__ == "__main__":
    main()