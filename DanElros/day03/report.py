import students_data


def calculate_average_age(data):
    """
    Рассчитывает средний возраст студентов.
    """
    if not data:
        return 0
    total_age = sum(student["age"] for student in data)
    return total_age / len(data)


def print_student_table(students):
    """
    Выводит таблицу студентов.
    """
    print(f"{'Имя':<15} {'Возраст':<10} {'Средний балл':<15}")
    print("-" * 45)
    for student in students:
        avg = students_data.avg_grade(student)
        print(f"{student['name']:<15} {student['age']:<10} {avg:<15.2f}")


def main():
    students = students_data.get_students()

    total_students = len(students)
    top_students = students_data.best_students(students, top=3)
    average_age = calculate_average_age(students)
    unique_names_set = students_data.unique_names(students)

    # Вывод отчёта
    print("=" * 50)
    print("ОТЧЁТ ПО СТУДЕНТАМ".center(50))
    print("=" * 50)

    print(f"\n1. Общая информация:")
    print(f"   Количество студентов: {total_students}")
    print(f"   Средний возраст: {average_age:.1f} лет")

    print(f"\n2. Топ-3 студента по успеваемости:")
    for i, student in enumerate(top_students, 1):
        avg = student.get("avg_grade", students_data.avg_grade(student))
        print(f"   {i}. {student['name']} (возраст: {student['age']}, "
              f"средний балл: {avg:.2f})")

    print(f"\n3. Уникальные имена студентов ({len(unique_names_set)} шт.):")
    unique_names_sorted = sorted(unique_names_set)
    print("   " + ", ".join(unique_names_sorted))

    print(f"\n4. Все студенты (отсортированные по возрасту):")
    sorted_by_age = students_data.sort_by_age(students)
    print_student_table(sorted_by_age)

    print("\n" + "=" * 50)
    print("Отчёт завершён.".center(50))
    print("=" * 50)


if __name__ == "__main__":
    main()