def is_prime(n):
    """
    Проверяет, является ли число простым.
    Возвращает True для простых чисел, False для составных и чисел <= 1.
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


def test_primes(limit=100):
    """
    Тестирует функцию is_prime на диапазоне от 1 до limit.
    Выводит список всех простых чисел в диапазоне.
    """
    primes = []
    for num in range(1, limit + 1):
        if is_prime(num):
            primes.append(num)

    print(f"Простые числа от 1 до {limit}:")
    for prime in primes:
        print(prime, end=" ")
    print(f"\n\nВсего найдено: {len(primes)}")
    return primes


if __name__ == "__main__":
    test_primes(100)