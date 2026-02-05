import csv
import logging


def load_data(file_path):
    """
    Загружает данные из CSV файла.
    Возвращает список словарей или пустой список при ошибке.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Загрузка данных из {file_path}")

    data = []
    skipped = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            try:
                header = next(reader)
            except StopIteration:
                logger.error("Файл пустой")
                return []

            for row_num, row in enumerate(reader, 2):
                if len(row) < 3:
                    logger.warning(f"Строка {row_num}: мало колонок")
                    skipped += 1
                    continue

                name = row[0].strip()
                subject = row[1].strip()
                score_str = row[2].strip()

                if not name or not subject or not score_str:
                    logger.warning(f"Строка {row_num}: пустые значения")
                    skipped += 1
                    continue

                try:
                    score = float(score_str)
                    if score < 2 or score > 5:
                        logger.warning(f"Строка {row_num}: оценка {score} вне диапазона 2-5")
                        skipped += 1
                        continue
                except ValueError:
                    logger.warning(f"Строка {row_num}: '{score_str}' не число")
                    skipped += 1
                    continue

                data.append({
                    'student': name,
                    'subject': subject,
                    'score': score
                })

        logger.info(f"Загружено {len(data)} записей, пропущено {skipped}")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return []