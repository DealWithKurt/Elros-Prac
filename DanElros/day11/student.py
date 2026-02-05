"""
Класс студента.
"""


class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        if 2 <= grade <= 5:
            self.grades.append(grade)
            return True
        return False

    def avg(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def as_dict(self):
        return {
            'name': self.name,
            'grades': self.grades,
            'average': self.avg()
        }

    def __str__(self):
        return f"Студент {self.name}, средний балл: {self.avg():.2f}"