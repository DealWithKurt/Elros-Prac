import tempfile
import os
from pathlib import Path


def read_numbers_from_file(filename):
    """
    Читает числа из файла, игнорируя некорректные строки.
    Возвращает список чисел.
    """
    numbers = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    number = float(line)
                    numbers.append(number)
                except ValueError:

                    print(f"Предупреждение: строка {line_num} '{line}' не является числом, пропущена")
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден")
        return []
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    return numbers


def calculate_statistics(numbers):
    """
    Вычисляет статистику по списку чисел.
    Возвращает словарь с результатами.
    """
    if not numbers:
        return {
            'count': 0,
            'min': None,
            'max': None,
            'average': None
        }

    return {
        'count': len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'average': sum(numbers) / len(numbers)
    }


def save_report_with_atomic_write(stats, output_filename):
    """
    Сохраняет отчет во временный файл, затем атомарно переименовывает его.
    """
    report = f"""СТАТИСТИКА ПО ЧИСЛАМ ИЗ ФАЙЛА
{'=' * 40}
Количество корректных чисел: {stats['count']}
Минимальное значение: {stats['min']}
Максимальное значение: {stats['max']}
Среднее значение: {stats['average']:.2f}
{'=' * 40}
Дата генерации отчета: {stats['timestamp']}
Файл с числами: {stats['source_file']}
"""

    temp_dir = Path(output_filename).parent
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                     dir=temp_dir, delete=False) as temp_file:
        temp_file.write(report)
        temp_filename = temp_file.name

    os.replace(temp_filename, output_filename)


def main():
    input_file = 'io_tasks/numbers.txt'
    output_file = 'io_tasks/result.txt'

    print("Чтение чисел из файла...")
    numbers = read_numbers_from_file(input_file)

    if not numbers:
        print("Не удалось прочитать числа. Проверьте файл numbers.txt")
        return

    print(f"Успешно прочитано {len(numbers)} чисел")

    stats = calculate_statistics(numbers)
    stats['timestamp'] = '2026-01-19'
    stats['source_file'] = input_file

    save_report_with_atomic_write(stats, output_file)
    print(f"Отчет сохранен в {output_file}")

    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТ:")
    print(f"Количество чисел: {stats['count']}")
    print(f"Минимум: {stats['min']}")
    print(f"Максимум: {stats['max']}")
    print(f"Среднее: {stats['average']:.2f}")


if __name__ == "__main__":
    main()