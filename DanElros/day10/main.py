import argparse
import logging
import sys
import os
from datetime import datetime

import load_csv
import analyze
import plot


def setup_logging():
    """Настройка логирования."""
    os.makedirs('logs', exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/student_{timestamp}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def create_test_data(filename, count=100):
    """Создание тестового CSV файла."""
    import csv
    import random

    students = ['Иванов Иван', 'Петрова Анна', 'Сидоров Сергей',
                'Кузнецова Мария', 'Смирнов Алексей']
    subjects = ['Математика', 'Физика', 'Химия', 'История', 'Литература']

    data = []
    for i in range(count):
        student = random.choice(students)
        subject = random.choice(subjects)
        score = round(random.uniform(2, 5), 1)
        data.append([student, subject, score])

    os.makedirs('data', exist_ok=True)

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Имя', 'Предмет', 'Оценка'])
        writer.writerows(data)

    print(f"Создан файл: {filename}")
    print(f"Записей: {count}")


def main():
    """Основная функция."""
    parser = argparse.ArgumentParser(description='Статистика студентов')
    parser.add_argument('csv_file', nargs='?', help='CSV файл с данными')
    parser.add_argument('--create', help='Создать тестовый файл')
    parser.add_argument('--count', type=int, default=100, help='Количество записей для теста')

    args = parser.parse_args()

    logger = setup_logging()

    print("=" * 50)
    print("СТАТИСТИКА СТУДЕНТОВ")
    print("=" * 50)

    if args.create:
        filename = f"data/{args.create}"
        create_test_data(filename, args.count)
        print(f"\nДля анализа запустите:")
        print(f"python main.py {filename}")
        return 0

    if not args.csv_file:
        print("Ошибка: укажите CSV файл")
        print("\nПримеры:")
        print("  python main.py данные.csv")
        print("  python main.py --create test.csv")
        return 1

    if not os.path.exists(args.csv_file):
        print(f"Файл не найден: {args.csv_file}")
        return 1

    print(f"\nЗагрузка: {args.csv_file}")
    data = load_csv.load_data(args.csv_file)

    if not data:
        print("Нет данных для анализа")
        return 1

    print("Анализ данных...")
    results = analyze.analyze_data(data)

    print("Создание отчета...")
    report = analyze.create_report(results)

    os.makedirs('reports', exist_ok=True)
    report_file = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Отчет сохранен: {report_file}")

    print("Создание графиков...")
    os.makedirs('figures', exist_ok=True)

    plot1 = plot.plot_subjects(results['subjects'], 'figures/subjects.png')
    plot2 = plot.plot_scores(results['score_counts'], 'figures/scores.png')
    plot3 = plot.plot_top_students(results['top_students'], 'figures/top.png')

    if plot1 and plot2 and plot3:
        print("Графики сохранены в figures/")

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 50)

    o = results['overall']
    print(f"\nОбщее:")
    print(f"  Записей: {o['total']}, Студентов: {o['students']}, Предметов: {o['subjects']}")
    print(f"  Средний балл: {o['avg_all']:.2f}")

    print(f"\nТоп студентов:")
    for i, (student, avg) in enumerate(results['top_students'], 1):
        print(f"  {i}. {student}: {avg:.2f}")

    print(f"\nЛучший предмет:")
    best_subject = max(results['subjects'].items(), key=lambda x: x[1]['average'])
    print(f"  {best_subject[0]}: {best_subject[1]['average']:.2f}")

    print("\n" + "=" * 50)
    print("Готово!")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())