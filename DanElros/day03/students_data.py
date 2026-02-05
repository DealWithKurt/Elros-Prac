def get_students():
    """
    Возвращает список словарей с данными студентов.
    """
    students = [
        {"name": "Иван", "age": 18, "grades": [5, 4, 3, 5]},
        {"name": "Мария", "age": 19, "grades": [5, 5, 5, 4]},
        {"name": "Алексей", "age": 20, "grades": [3, 4, 4, 3]},
        {"name": "Екатерина", "age": 18, "grades": [4, 5, 5, 5]},
        {"name": "Дмитрий", "age": 21, "grades": [3, 3, 4, 4]},
        {"name": "Анна", "age": 19, "grades": [5, 4, 5, 4]},
        {"name": "Сергей", "age": 22, "grades": [4, 4, 3, 4]},
        {"name": "Ольга", "age": 18, "grades": [5, 5, 4, 5]},
        {"name": "Павел", "age": 20, "grades": [4, 3, 4, 3]},
        {"name": "Иван", "age": 19, "grades": [4, 4, 4, 4]},
        {"name": "Наталья", "age": 21, "grades": [5, 5, 5, 5]},
        {"name": "Александр", "age": 20, "grades": [3, 4, 3, 4]}
    ]
    return students


def sort_by_age(data, reverse=False):
    """
    Возвращает новый список, отсортированный по возрасту.
    Не изменяет исходные данные.
    """
    return sorted(data, key=lambda student: student["age"], reverse=reverse)


def avg_grade(student):
    """
    Рассчитывает средний балл студента.
    """
    grades = student["grades"]
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def best_students(data, top=3):
    """
    Возвращает top-N студентов по среднему баллу (от лучшего к худшему).
    """
    students_with_avg = []
    for student in data:
        student_copy = student.copy()
        student_copy["avg_grade"] = avg_grade(student)
        students_with_avg.append(student_copy)

    sorted_students = sorted(students_with_avg, key=lambda s: s["avg_grade"], reverse=True)
    return sorted_students[:top]


def unique_names(data):
    """
    Возвращает множество уникальных имён.
    """
    names = set()
    for student in data:
        names.add(student["name"])
    return names