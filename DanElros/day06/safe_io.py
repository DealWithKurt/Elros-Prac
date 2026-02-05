"""
Модуль для безопасного чтения файлов с числами и расчета статистики.
"""

import logging
import traceback
from pathlib import Path

# Настройка логгера
logger = logging.getLogger(__name__)


def read_numbers_from_file(file_path):
    """
    Читает числа из файла, пропускает некорректные строки.
    Возвращает список чисел.
    """
    numbers = []
    line_count = 0
    skipped_lines = 0

    try:
        logger.info(f"Начало чтения файла: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line_count += 1
                line = line.strip()

                if not line:
                    continue

                try:
                    number = float(line)
                    numbers.append(number)
                except ValueError:
                    skipped_lines += 1
                    logger.warning(f"Строка {line_num}: '{line}' не является числом, пропущена")

        if skipped_lines > 0:
            logger.warning(f"Пропущено {skipped_lines} некорректных строк")

        logger.info(f"Прочитано {len(numbers)} чисел из {line_count} строк")
        return numbers

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return None
    except PermissionError:
        logger.error(f"Нет прав на чтение файла: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {str(e)}")
        logger.debug(f"Трассировка:\n{traceback.format_exc()}")
        return None


def calculate_statistics(numbers):
    """
    Рассчитывает статистику по списку чисел.
    Возвращает словарь с результатами.
    """
    if not numbers:
        logger.error("Список чисел пустой")
        return None

    try:
        logger.info(f"Расчет статистики для {len(numbers)} чисел")

        stats = {
            'count': len(numbers),
            'min': min(numbers),
            'max': max(numbers),
            'sum': sum(numbers),
            'average': sum(numbers) / len(numbers)
        }

        logger.info("Статистика рассчитана успешно")
        return stats

    except Exception as e:
        logger.error(f"Ошибка при расчете статистики: {str(e)}")
        logger.debug(f"Трассировка:\n{traceback.format_exc()}")
        return None


def process_file(file_path):
    """
    Основная функция обработки файла.
    Читает числа и рассчитывает статистику.
    """
    logger.info(f"Начало обработки файла: {file_path}")

    numbers = read_numbers_from_file(file_path)
    if numbers is None:
        return None

    stats = calculate_statistics(numbers)
    if stats is None:
        return None

    logger.info("Обработка файла завершена успешно")
    return stats


def format_report(stats, file_path):
    """
    Форматирует отчет со статистикой.
    """
    if stats is None:
        return "Не удалось обработать файл"

    report = f"""
{'=' * 50}
ОТЧЕТ ПО ФАЙЛУ: {file_path}
{'=' * 50}
Количество чисел: {stats['count']}
Минимальное значение: {stats['min']}
Максимальное значение: {stats['max']}
Сумма чисел: {stats['sum']}
Среднее значение: {stats['average']:.2f}
{'=' * 50}
"""
    return report