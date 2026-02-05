"""
Базовый класс Person и его наследники.
"""
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        return f"Человек: {self.name}, {self.age} лет"

    def __str__(self):
        return self.info()


class Student(Person):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.grades = []

    def add_grade(self, grade):
        if 2 <= grade <= 5:
            self.grades.append(grade)
            return True
        return False

    def avg_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def info(self):
        avg = self.avg_grade()
        grades_str = ", ".join(str(g) for g in self.grades) if self.grades else "нет"
        return f"Студент: {self.name}, {self.age} лет, оценки: [{grades_str}], средний: {avg:.2f}"

    def __lt__(self, other):
        return self.avg_grade() < other.avg_grade()

    def __eq__(self, other):
        return self.avg_grade() == other.avg_grade()

    def __le__(self, other):
        return self.avg_grade() <= other.avg_grade()

    def __gt__(self, other):
        return self.avg_grade() > other.avg_grade()

    def __ge__(self, other):
        return self.avg_grade() >= other.avg_grade()


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def info(self):
        return f"Учитель: {self.name}, {self.age} лет, предмет: {self.subject}"