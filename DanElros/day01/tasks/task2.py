def process_numbers():
    numbers = [5, 12, 8, 3, 19, 7, 14, 2, 20, 11, 6, 17, 4, 9, 13, 1, 16, 10, 15, 18]

    even_numbers = [num for num in numbers if num % 2 == 0]
    sum_even = sum(even_numbers)
    avg_even = sum_even / len(even_numbers) if even_numbers else 0

    print(f"Исходный список: {numbers}")
    print(f"Четные числа: {even_numbers}")
    print(f"Сумма четных чисел: {sum_even}")
    print(f"Среднее значение четных чисел: {avg_even:.2f}")


if __name__ == "__main__":
    process_numbers()