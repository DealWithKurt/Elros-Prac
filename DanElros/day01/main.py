def main():

    name = input("Введите ваше имя: ").strip()
    group = input("Введите вашу группу: ").strip()
    interests = input("Введите ваши интересы (через запятую): ").strip()

    print(f"Имя: {name}")
    print(f"Группа: {group}")
    print(f"Интересы: {interests}")

if __name__ == "__main__":
    main()