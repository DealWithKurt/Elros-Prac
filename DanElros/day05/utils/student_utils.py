def avg_grade(student):
    """
    Рассчитывает средний балл студента.

    """
    grades = student.get('grades')
    if grades is None:
        raise KeyError("У студента отсутствует ключ 'grades'")

    if not grades:
        raise ValueError("Список оценок не может быть пустым")

    return sum(grades) / len(grades)


def sort_by_age(students, reverse=False):
    """
    Сортирует список студентов по возрасту.

    """
    return sorted(students, key=lambda s: s.get('age', 0), reverse=reverse)


def best_students(students, top=3):
    """
    Возвращает топ-N студентов по среднему баллу.

    """
    students_with_avg = []
    for student in students:
        try:
            avg = avg_grade(student)
            student_copy = student.copy()
            student_copy['avg_grade'] = avg
            students_with_avg.append(student_copy)
        except (KeyError, ValueError):
            continue

    sorted_students = sorted(students_with_avg,
                             key=lambda s: s['avg_grade'],
                             reverse=True)
    return sorted_students[:top]


def unique_names(students):
    """
    Возвращает множество уникальных имен студентов.

    """
    names = set()
    for student in students:
        name = student.get('name')
        if name:
            names.add(name)
    return names