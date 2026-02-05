import calc


def parse_input(user_input):
    """
    Пытается разобрать ввод пользователя на три компонента.
    Возвращает (num1, op, num2) или None при ошибке.
    """
    parts = user_input.split()
    if len(parts) != 3:
        return None

    try:
        num1 = float(parts[0])
        num2 = float(parts[2])
    except ValueError:
        return None

    op = parts[1]
    if op not in ['+', '-', '*', '/']:
        return None

    return num1, op, num2


def calculate(num1, op, num2):
    """
    Выполняет операцию с помощью модуля calc.
    """
    if op == '+':
        return calc.add(num1, num2)
    elif op == '-':
        return calc.sub(num1, num2)
    elif op == '*':
        return calc.mul(num1, num2)
    elif op == '/':
        return calc.div(num1, num2)


def main():
    print("Калькулятор (для выхода введите 'exit')")
    print("Формат ввода: число операция число")
    print("Пример: 5 * 7")

    while True:
        user_input = input("\n> ").strip()

        if user_input.lower() == 'exit':
            print("Выход из калькулятора.")
            break

        parsed = parse_input(user_input)
        if parsed is None:
            print("Ошибка: некорректный формат.")
            print("Используйте: число операция число (например: 5 * 7)")
            continue

        num1, op, num2 = parsed
        result = calculate(num1, op, num2)

        if result is not None:
            print(f"Результат: {num1} {op} {num2} = {result}")


if __name__ == "__main__":
    main()