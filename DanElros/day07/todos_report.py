"""
Скрипт для анализа задач и генерации отчета.
"""

import json
from collections import Counter
from pathlib import Path


def load_todos_from_file(file_path):
    """
    Загружает задачи из JSON файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            todos = json.load(f)

        print(f"Загружено задач: {len(todos)}")
        return todos

    except FileNotFoundError:
        print(f"Ошибка: файл не найден - {file_path}")
        print("Сначала запустите fetch_todos.py")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка: неверный JSON в файле {file_path}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def analyze_todos(todos):
    """
    Анализирует задачи и возвращает статистику.
    """
    if not todos:
        return None

    total_tasks = len(todos)
    completed_tasks = sum(1 for todo in todos if todo.get('completed') == True)
    incomplete_tasks = total_tasks - completed_tasks

    user_completed = Counter()
    for todo in todos:
        if todo.get('completed') == True:
            user_id = todo.get('userId')
            if user_id is not None:
                user_completed[user_id] += 1

    top_users = user_completed.most_common(3)

    all_users = set(todo.get('userId') for todo in todos if todo.get('userId') is not None)

    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
        'completion_rate': (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
        'total_users': len(all_users),
        'top_users': top_users,
        'user_completed': dict(user_completed)
    }


def main():
    """
    Основная функция.
    """
    input_file = "data/todos.json"

    print("=" * 50)
    print("Анализ задач")
    print("=" * 50)

    todos = load_todos_from_file(input_file)
    if todos is None:
        return 1

    stats = analyze_todos(todos)

    print("\n" + "=" * 50)
    print("ОТЧЕТ")
    print("=" * 50)

    print(f"\nОбщая статистика:")
    print(f"  Всего задач: {stats['total_tasks']}")
    print(f"  Выполнено: {stats['completed_tasks']}")
    print(f"  Не выполнено: {stats['incomplete_tasks']}")
    print(f"  Процент выполнения: {stats['completion_rate']:.1f}%")
    print(f"  Всего пользователей: {stats['total_users']}")

    print(f"\nТоп-3 пользователей по выполненным задачам:")
    for i, (user_id, count) in enumerate(stats['top_users'], 1):
        print(f"  {i}. Пользователь {user_id}: {count} выполненных задач")

    print("\n" + "=" * 50)
    print("Статистика по всем пользователям:")
    for user_id in sorted(stats['user_completed'].keys()):
        count = stats['user_completed'][user_id]
        print(f"  Пользователь {user_id}: {count} выполненных задач")

    print("\n" + "=" * 50)

    print("\nПримеры задач из файла:")
    print("-" * 40)

    for i, todo in enumerate(todos[:5], 1):
        status = "✓ Выполнена" if todo['completed'] else "✗ Не выполнена"
        print(f"{i}. {todo['title']}")
        print(f"   Пользователь: {todo['userId']}, Статус: {status}")
        print()

    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)