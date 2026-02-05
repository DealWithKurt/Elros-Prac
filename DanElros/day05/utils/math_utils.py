def add(a, b):
    """
    Складывает два числа.

    """
    return a + b


def sub(a, b):
    """
    Вычитает второе число из первого.

    """
    return a - b


def mul(a, b):
    """
    Умножает два числа.

    """
    return a * b


def div(a, b):
    """
    Делит первое число на второе.

    """
    if b == 0:
        raise ValueError("Деление на ноль недопустимо")
    return a / b


def is_prime(n):
    """
    Проверяет, является ли число простым.

    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def calculate_statistics(numbers):
    """
    Вычисляет базовую статистику по списку чисел.

    """
    if not numbers:
        return {
            'count': 0,
            'min': None,
            'max': None,
            'average': None
        }

    return {
        'count': len(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'average': sum(numbers) / len(numbers)
    }