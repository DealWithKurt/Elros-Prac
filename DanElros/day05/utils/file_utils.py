import tempfile
import os
import json
from pathlib import Path


def read_numbers_from_file(filename):
    """
    Читает числа из текстового файла.
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
                    continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except IOError as e:
        raise IOError(f"Ошибка при чтении файла {filename}: {e}")

    return numbers


def save_with_atomic_write(content, filename):
    """
    Сохраняет содержимое в файл с атомарной записью.

    """
    temp_dir = Path(filename).parent
    temp_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                     dir=temp_dir, delete=False) as temp_file:
        temp_file.write(content)
        temp_filename = temp_file.name

    os.replace(temp_filename, filename)


def load_json_file(filename):
    """
    Загружает данные из JSON файла.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Невалидный JSON в файле {filename}",
                                   e.doc, e.pos)


def save_json_file(data, filename):
    """
    Сохраняет данные в JSON файл.

    """
    temp_dir = Path(filename).parent
    temp_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                     dir=temp_dir, delete=False) as temp_file:
        json.dump(data, temp_file, ensure_ascii=False, indent=2)
        temp_filename = temp_file.name

    os.replace(temp_filename, filename)