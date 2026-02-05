# День 5. Функции, модули, докстринги, простейшие тесты.


## Описание модулей

### utils.math_utils
Математические функции из предыдущих дней:
- `add(a, b)` - сложение
- `sub(a, b)` - вычитание
- `mul(a, b)` - умножение
- `div(a, b)` - деление с проверкой на ноль
- `is_prime(n)` - проверка числа на простоту
- `calculate_statistics(numbers)` - статистика по списку чисел

### utils.student_utils
Функции для работы с данными студентов:
- `avg_grade(student)` - средний балл студента
- `sort_by_age(students, reverse=False)` - сортировка по возрасту
- `best_students(students, top=3)` - топ студентов по успеваемости
- `unique_names(students)` - уникальные имена

### utils.file_utils
Функции для работы с файлами:
- `read_numbers_from_file(filename)` - чтение чисел из текстового файла
- `save_with_atomic_write(content, filename)` - атомарная запись в файл
- `load_json_file(filename)` - загрузка JSON файла
- `save_json_file(data, filename)` - сохранение в JSON файл

## Запуск тестов

### Вариант 1: Запуск всех тестов
```bash
    python test_utils.py