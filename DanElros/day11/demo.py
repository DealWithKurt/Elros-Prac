"""
Демонстрация работы классов Student и Group.
"""
from student import Student
from group import Group


def main():
    print("=" * 50)
    print("Демонстрация классов Student и Group")
    print("=" * 50)

    print("\n1. Создаем студентов:")

    student1 = Student("Иванов Иван")
    student1.add_grade(4)
    student1.add_grade(5)
    student1.add_grade(3)
    print(f"   {student1}")

    student2 = Student("Петрова Анна")
    student2.add_grade(5)
    student2.add_grade(5)
    student2.add_grade(4)
    print(f"   {student2}")

    student3 = Student("Сидоров Сергей")
    student3.add_grade(3)
    student3.add_grade(4)
    student3.add_grade(4)
    print(f"   {student3}")

    student4 = Student("Кузнецова Мария")
    student4.add_grade(4)
    student4.add_grade(4)
    student4.add_grade(5)
    print(f"   {student4}")

    student5 = Student("Смирнов Алексей")
    student5.add_grade(2)
    student5.add_grade(3)
    student5.add_grade(3)
    print(f"   {student5}")

    print("\n2. Создаем группу:")
    group = Group("РПО-23")
    print(f"   {group}")

    print("\n3. Добавляем студентов в группу:")
    group.add_student(student1)
    group.add_student(student2)
    group.add_student(student3)
    group.add_student(student4)
    group.add_student(student5)
    print(f"   Добавлено студентов: {len(group.students)}")

    print(f"\n4. Средний балл по группе: {group.avg_all():.2f}")

    print("\n5. Топ-3 студента:")
    top_students = group.best(3)
    for i, student in enumerate(top_students, 1):
        print(f"   {i}. {student.name} - {student.avg():.2f}")

    print("\n6. Данные студентов в виде словаря:")
    for student in group.students[:2]:
        data = student.as_dict()
        print(f"   {student.name}: {data}")

    print("\n" + "=" * 50)
    print("Демонстрация завершена")
    print("=" * 50)


if __name__ == "__main__":
    main()