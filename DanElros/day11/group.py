"""
Класс группы студентов.
"""

from student import Student


class Group:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        if isinstance(student, Student):
            self.students.append(student)
            return True
        return False

    def best(self, n=3):
        if not self.students:
            return []

        sorted_students = sorted(self.students, key=lambda s: s.avg(), reverse=True)
        return sorted_students[:n]

    def avg_all(self):
        if not self.students:
            return 0

        total = sum(student.avg() for student in self.students)
        return total / len(self.students)

    def __str__(self):
        return f"Группа: {self.name}, студентов: {len(self.students)}"