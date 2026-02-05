def normalize_name(s):
    s = s.strip()
    words = s.split()
    normalized_words = []
    for word in words:
        if word:
            normalized_words.append(word.title())
    return " ".join(normalized_words)


def test_normalize_name():
    test_cases = [
        "  Мария Иванова  ",
        "алексей   второй",
        "боб перый  Олегович   ",
        "  двойной  пробел  тест  "
    ]

    for test in test_cases:
        result = normalize_name(test)
        print(f"'{test}' - '{result}'")


if __name__ == "__main__":
    test_normalize_name()