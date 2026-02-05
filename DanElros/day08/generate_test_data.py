"""
Скрипт для генерации тестового CSV файла с оценками студентов.
"""

import csv
import random
from pathlib import Path


def generate_students_scores():
    """
    Генерирует тестовые данные об оценках студентов.
    """
    first_names = ["Иван", "Анна", "Сергей", "Мария", "Алексей", "Екатерина",
                   "Дмитрий", "Ольга", "Андрей", "Наталья", "Павел", "Юлия",
                   "Михаил", "Антон", "Татьяна", "Владимир", "Елена", "Николай"]

    last_names = ["Иванов", "Петров", "Сидоров", "Смирнов", "Кузнецов", "Попов",
                  "Васильев", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев"]

    subjects = ["Математика", "Физика", "Химия", "История", "Литература",
                "Английский язык", "Информатика", "Биология", "География"]

    data = []
    student_id = 1

    for first_name in first_names:
        for last_name in last_names[:5]:
            student_name = f"{last_name} {first_name}"

            for subject in random.sample(subjects, random.randint(3, 6)):
                base_score = random.randint(2, 5)
                if random.random() > 0.7:
                    score = base_score + random.choice([-0.3, -0.2, 0.2, 0.3])
                    score = round(score, 1)
                else:
                    score = float(base_score)

                data.append([student_name, subject, score])

            student_id += 1
            if student_id > 50:
                break
        if student_id > 50:
            break

    bad_data = [
        ["", "Математика", "4.5"],
        ["Петров Иван", "", "3.8"],
        ["Сидоров Сергей", "Физика", ""],
        ["Иванов Анна", "Химия", "не число"],
        ["", "", ""],
        ["Кузнецов Дмитрий", "История", "6"],
        ["Попова Мария", "Литература", "1"],
    ]

    data.extend(bad_data)
    random.shuffle(data)

    return data


def save_to_csv(data, file_path):
    """
    Сохраняет данные в CSV файл.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Имя', 'Предмет', 'Оценка'])
            writer.writerows(data)

        print(f"Данные сохранены в: {file_path}")
        print(f"Количество строк: {len(data)}")
        return True

    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False


def main():
    """
    Основная функция.
    """
    output_file = "data/students_scores.csv"

    print("=" * 50)
    print("Генерация тестовых данных об оценках")
    print("=" * 50)

    print("Генерация данных...")
    data = generate_students_scores()

    if save_to_csv(data, output_file):
        print("\nПервые 5 строк данных:")
        print("-" * 40)
        for i, row in enumerate(data[:5], 1):
            print(f"{i}. {row}")

        print("\n" + "=" * 50)
        print("Генерация завершена успешно!")
        print("Для анализа запустите: python csv_stats.py")
        return 0
    else:
        print("Ошибка при сохранении данных")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)