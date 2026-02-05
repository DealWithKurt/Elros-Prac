"""
Скрипт для анализа CSV файла с оценками студентов.
"""

import csv
import statistics
from collections import defaultdict, Counter
from pathlib import Path


def load_csv_data(file_path):
    """
    Загружает данные из CSV файла.
    Возвращает список корректных записей.
    """
    data = []
    skipped_lines = 0
    line_num = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
                line_num += 1
            except StopIteration:
                print("Файл пустой")
                return [], 0

            for row in reader:
                line_num += 1

                if len(row) < 3:
                    print(f"Строка {line_num}: недостаточно колонок, пропущена")
                    skipped_lines += 1
                    continue

                name = row[0].strip()
                subject = row[1].strip()
                score_str = row[2].strip()

                if not name or not subject or not score_str:
                    print(f"Строка {line_num}: пустое значение, пропущена")
                    skipped_lines += 1
                    continue

                try:
                    score = float(score_str)
                except ValueError:
                    print(f"Строка {line_num}: оценка '{score_str}' не является числом, пропущена")
                    skipped_lines += 1
                    continue

                if score < 2 or score > 5:
                    print(f"Строка {line_num}: оценка {score} вне диапазона 2-5, пропущена")
                    skipped_lines += 1
                    continue

                data.append({
                    'name': name,
                    'subject': subject,
                    'score': score
                })

        print(f"Загружено корректных записей: {len(data)}")
        print(f"Пропущено строк: {skipped_lines}")
        return data, skipped_lines

    except FileNotFoundError:
        print(f"Ошибка: файл не найден - {file_path}")
        print("Сначала запустите generate_test_data.py")
        return [], 0
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], 0


def calculate_statistics(data):
    """
    Рассчитывает статистику по данным.
    """
    if not data:
        return None

    subject_scores = defaultdict(list)
    student_scores = defaultdict(list)

    for record in data:
        subject_scores[record['subject']].append(record['score'])
        student_scores[record['name']].append(record['score'])

    subject_stats = {}
    for subject, scores in subject_scores.items():
        subject_stats[subject] = {
            'count': len(scores),
            'average': statistics.mean(scores),
            'min': min(scores),
            'max': max(scores)
        }

    student_averages = {}
    for student, scores in student_scores.items():
        student_averages[student] = statistics.mean(scores)

    top_students = sorted(student_averages.items(),
                          key=lambda x: x[1],
                          reverse=True)[:5]

    all_scores = [record['score'] for record in data]
    total_students = len(student_scores)
    total_subjects = len(subject_scores)

    return {
        'total_records': len(data),
        'total_students': total_students,
        'total_subjects': total_subjects,
        'overall_average': statistics.mean(all_scores),
        'overall_min': min(all_scores),
        'overall_max': max(all_scores),
        'subject_stats': subject_stats,
        'top_students': top_students,
        'student_averages': student_averages
    }


def save_report(stats, file_path):
    """
    Сохраняет отчет в текстовый файл.
    """
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("ОТЧЕТ ПО ОЦЕНКАМ СТУДЕНТОВ\n")
            f.write("=" * 60 + "\n\n")

            f.write("ОБЩАЯ СТАТИСТИКА:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Всего записей: {stats['total_records']}\n")
            f.write(f"Всего студентов: {stats['total_students']}\n")
            f.write(f"Всего предметов: {stats['total_subjects']}\n")
            f.write(f"Средний балл по всем предметам: {stats['overall_average']:.2f}\n")
            f.write(f"Минимальная оценка: {stats['overall_min']:.1f}\n")
            f.write(f"Максимальная оценка: {stats['overall_max']:.1f}\n\n")

            f.write("СТАТИСТИКА ПО ПРЕДМЕТАМ:\n")
            f.write("-" * 40 + "\n")
            for subject, stat in sorted(stats['subject_stats'].items()):
                f.write(f"{subject}:\n")
                f.write(f"  Количество оценок: {stat['count']}\n")
                f.write(f"  Средний балл: {stat['average']:.2f}\n")
                f.write(f"  Диапазон: {stat['min']:.1f}-{stat['max']:.1f}\n\n")

            f.write("ТОП-5 СТУДЕНТОВ:\n")
            f.write("-" * 40 + "\n")
            for i, (student, avg) in enumerate(stats['top_students'], 1):
                f.write(f"{i}. {student}: {avg:.2f}\n")
            f.write("\n")

            f.write("ВСЕ СТУДЕНТЫ (по среднему баллу):\n")
            f.write("-" * 40 + "\n")
            for student, avg in sorted(stats['student_averages'].items(),
                                       key=lambda x: x[1],
                                       reverse=True):
                f.write(f"  {student}: {avg:.2f}\n")

            f.write("\n" + "=" * 60 + "\n")
            f.write("Отчет сгенерирован автоматически\n")
            f.write("=" * 60 + "\n")

        print(f"Отчет сохранен в: {file_path}")
        return True

    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")
        return False


def main():
    """
    Основная функция.
    """
    input_file = "data/students_scores.csv"
    output_file = "reports/csv_stats.txt"

    print("=" * 50)
    print("Анализ оценок студентов из CSV файла")
    print("=" * 50)

    data, skipped = load_csv_data(input_file)

    if not data:
        print("Нет данных для анализа")
        return 1

    print("\nРасчет статистики...")
    stats = calculate_statistics(data)

    if not stats:
        print("Не удалось рассчитать статистику")
        return 1

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 50)

    print(f"\nОбщая статистика:")
    print(f"  Всего записей: {stats['total_records']}")
    print(f"  Всего студентов: {stats['total_students']}")
    print(f"  Всего предметов: {stats['total_subjects']}")
    print(f"  Средний балл: {stats['overall_average']:.2f}")

    print(f"\nСтатистика по предметам:")
    for subject, stat in sorted(stats['subject_stats'].items()):
        print(f"  {subject}: {stat['average']:.2f} (оценок: {stat['count']})")

    print(f"\nТоп-5 студентов:")
    for i, (student, avg) in enumerate(stats['top_students'], 1):
        print(f"  {i}. {student}: {avg:.2f}")

    print(f"\nСохранение отчета...")
    if save_report(stats, output_file):
        print("\n" + "=" * 50)
        print("Анализ завершен успешно!")
        print(f"Полный отчет в: {output_file}")
        print("=" * 50)
        return 0
    else:
        print("Ошибка при сохранении отчета")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)