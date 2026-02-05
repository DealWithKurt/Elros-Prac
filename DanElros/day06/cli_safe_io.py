"""
CLI интерфейс для безопасной обработки файлов с числами.
"""

import sys
import logging
import argparse
from pathlib import Path
from safe_io import process_file, format_report, logger


def setup_logging(log_file='logs/app.log', level=logging.INFO):
    """
    Настраивает логирование.
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.setLevel(level)


def create_test_file(file_path, count=20):
    """
    Создает тестовый файл с числами.
    """
    import random

    numbers = [random.randint(1, 100) for _ in range(count)]

    with open(file_path, 'w', encoding='utf-8') as f:
        for num in numbers:
            f.write(f"{num}\n")
        f.write("\n")
        f.write("abc\n")
        f.write("123abc\n")

    print(f"Создан тестовый файл: {file_path}")


def main():
    """
    Основная функция CLI.
    """
    parser = argparse.ArgumentParser(description='Обработка файлов с числами')
    parser.add_argument('file_path', nargs='?', help='Путь к файлу с числами')
    parser.add_argument('--create-test', help='Создать тестовый файл')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        default='INFO', help='Уровень логирования')

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level)
    setup_logging(level=log_level)

    if args.create_test:
        try:
            create_test_file(args.create_test)
            return 0
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}")
            return 1

    if not args.file_path:
        print("Ошибка: не указан файл для обработки")
        print("Используйте --help для просмотра справки")
        return 1

    file_path = Path(args.file_path)
    if not file_path.exists():
        logger.error(f"Файл не найден: {args.file_path}")
        print(f"Ошибка: файл '{args.file_path}' не найден")
        return 1

    print(f"Обработка файла: {args.file_path}")
    stats = process_file(args.file_path)

    if stats:
        report = format_report(stats, args.file_path)
        print(report)
        return 0
    else:
        print(f"\nНе удалось обработать файл: {args.file_path}")
        print("Проверьте логи в logs/app.log")
        return 1


if __name__ == '__main__':
    sys.exit(main())