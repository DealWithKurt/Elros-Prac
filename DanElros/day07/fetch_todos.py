"""
Скрипт для генерации задач с русскими названиями и сохранения в файл.
"""

import json
import random
from pathlib import Path


def generate_russian_todos(count=200):
    """
    Генерирует тестовые задачи с русскими названиями.
    """
    russian_titles = [
        "Купить продукты",
        "Сделать домашнее задание",
        "Позвонить маме",
        "Заплатить за квартиру",
        "Сходить в тренажерный зал",
        "Прочитать книгу",
        "Написать отчет",
        "Подготовиться к встрече",
        "Починить компьютер",
        "Убраться в комнате",
        "Записаться к врачу",
        "Забронировать билеты",
        "Изучить Python",
        "Создать проект",
        "Проверить почту",
        "Обновить резюме",
        "Приготовить ужин",
        "Полить цветы",
        "Сделать зарядку",
        "Посмотреть фильм",
        "Постирать одежду",
        "Сходить в банк",
        "Заправить машину",
        "Купить лекарства",
        "Отправить посылку"
    ]

    tasks = []
    for i in range(count):
        user_id = random.randint(1, 10)
        completed = random.choice([True, False])
        title = random.choice(russian_titles)

        task = {
            "userId": user_id,
            "id": i + 1,
            "title": f"{title}",
            "completed": completed
        }
        tasks.append(task)

    return tasks


def save_to_file(todos, file_path):
    """
    Сохраняет задачи в JSON файл.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)

        print(f"Данные сохранены в: {file_path}")
        print(f"Всего задач: {len(todos)}")
        return True

    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False


def main():
    """
    Основная функция.
    """
    output_file = "data/todos.json"

    print("=" * 50)
    print("Генерация задач с русскими названиями")
    print("=" * 50)

    print("Генерация 200 задач...")
    todos = generate_russian_todos(200)

    if save_to_file(todos, output_file):
        # Показываем примеры
        print("\nПримеры задач:")
        print("-" * 40)

        completed = [t for t in todos if t['completed']]
        not_completed = [t for t in todos if not t['completed']]

        print("Выполненные:")
        for i, todo in enumerate(completed[:3], 1):
            print(f"  {i}. {todo['title']} (Пользователь: {todo['userId']})")

        print("\nНе выполненные:")
        for i, todo in enumerate(not_completed[:3], 1):
            print(f"  {i}. {todo['title']} (Пользователь: {todo['userId']})")

        print("\n" + "=" * 50)
        print("Генерация завершена успешно!")
        print("Для анализа запустите: python todos_report.py")
        return 0
    else:
        print("Ошибка при сохранении данных")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)