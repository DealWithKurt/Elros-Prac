"""
Демонстрация наследования и полиморфизма.
"""

from person import Person, Student, Teacher


def main():
    print("=" * 50)
    print("Демонстрация наследования и полиморфизма")
    print("=" * 50)

    # Создаем список разных людей
    print("\n1. Создаем список людей (Person, Student, Teacher):")

    people = [
        Person("Иванов Иван", 25),
        Student("Петрова Анна", 20),
        Teacher("Сидорова Мария", 45, "Математика"),
        Student("Кузнецов Сергей", 21),
        Teacher("Попов Алексей", 38, "Физика"),
        Student("Смирнова Ольга", 19)
    ]

    people[1].add_grade(4)
    people[1].add_grade(5)
    people[1].add_grade(3)

    people[3].add_grade(5)
    people[3].add_grade(4)
    people[3].add_grade(5)

    people[5].add_grade(3)
    people[5].add_grade(4)
    people[5].add_grade(4)

    print("\n2. Полиморфизм - метод info() для всех:")
    print("-" * 50)
    for person in people:
        print(f"  {person.info()}")

    print("\n3. Создаем список только студентов:")
    students = []
    for person in people:
        if isinstance(person, Student):
            students.append(person)
            print(f"  {person.info()}")

    print("\n4. Сортировка студентов по среднему баллу:")
    sorted_students = sorted(students, reverse=True)
    for i, student in enumerate(sorted_students, 1):
        print(f"  {i}. {student.name} - средний: {student.avg_grade():.2f}")

    print("\n5. Сравнение студентов:")
    if len(students) >= 2:
        s1, s2 = students[0], students[1]
        print(f"  {s1.name} ({s1.avg_grade():.2f}) > {s2.name} ({s2.avg_grade():.2f}): {s1 > s2}")
        print(f"  {s1.name} ({s1.avg_grade():.2f}) < {s2.name} ({s2.avg_grade():.2f}): {s1 < s2}")
        print(f"  {s1.name} ({s1.avg_grade():.2f}) == {s2.name} ({s2.avg_grade():.2f}): {s1 == s2}")

    print("\n6. Проверка типов (isinstance):")
    for person in people[:3]:  # Первые три
        print(f"  {person.name}:")
        print(f"    Person: {isinstance(person, Person)}")
        print(f"    Student: {isinstance(person, Student)}")
        print(f"    Teacher: {isinstance(person, Teacher)}")

    print("\n" + "=" * 50)
    print("Демонстрация завершена")
    print("=" * 50)


if __name__ == "__main__":
    main()