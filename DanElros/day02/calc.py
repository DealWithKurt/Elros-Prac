def add(a, b):
    """
    Возвращает сумму двух чисел.
    """
    return a + b


def sub(a, b):
    """
    Возвращает разность двух чисел (a - b).
    """
    return a - b


def mul(a, b):
    """
    Возвращает произведение двух чисел.
    """
    return a * b


def div(a, b):
    """
    Возвращает результат деления a на b.
    При делении на ноль возвращает None и выводит сообщение.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None