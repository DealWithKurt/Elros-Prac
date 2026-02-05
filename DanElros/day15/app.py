from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'секретный-ключ-для-flask'

DATA_FILE = Path("data/students.json")

def load_students():
    """Загружает студентов из JSON файла при запуске."""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for student in data:
                    if isinstance(student.get('created_at'), str):
                        student['created_at'] = datetime.fromisoformat(student['created_at'])
                return data
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
            return []
    return []

def save_students():
    """Сохраняет текущий список студентов в JSON файл."""
    try:
        data_to_save = []
        for student in students:
            student_copy = student.copy()
            if isinstance(student_copy.get('created_at'), datetime):
                student_copy['created_at'] = student_copy['created_at'].isoformat()
            data_to_save.append(student_copy)

        DATA_FILE.parent.mkdir(exist_ok=True)

        temp_file = DATA_FILE.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2, default=str)

        temp_file.replace(DATA_FILE)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        return False

def get_next_id():
    """Генерирует следующий числовой ID для нового студента."""
    if not students:
        return 1

    max_id = 0
    for student in students:
        student_id = student.get('id')
        try:
            if isinstance(student_id, int):
                num_id = student_id
            elif isinstance(student_id, str):
                num_id = int(student_id)
            else:
                continue

            if num_id > max_id:
                max_id = num_id
        except (ValueError, TypeError):
            continue

    return max_id + 1

students = load_students()

@app.route('/')
def index():
    """Главная страница со списком студентов."""
    return render_template('index.html', students=students)


@app.route('/about')
def about():
    """Страница "О сайте"."""
    return render_template('about.html')


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Страница добавления студента."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '')

        # Проверяем данные
        if not name:
            flash('Введите имя студента', 'error')
            return render_template('add.html', students=students)

        if not age:
            flash('Введите возраст студента', 'error')
            return render_template('add.html', students=students)

        try:
            age_int = int(age)
            if age_int < 16 or age_int > 35:
                flash('Возраст должен быть от 16 до 35 лет', 'error')
                return render_template('add.html', students=students)
        except ValueError:
            flash('Возраст должен быть числом', 'error')
            return render_template('add.html', students=students)

        new_student = {
            'id': get_next_id(),
            'name': name,
            'age': age_int,
            'created_at': datetime.now()
        }

        students.append(new_student)

        if save_students():
            flash(f'Студент {name} успешно добавлен и сохранен!', 'success')
        else:
            flash(f'Студент {name} добавлен, но произошла ошибка при сохранении', 'warning')

        return redirect(url_for('index'))

    return render_template('add.html', students=students)


@app.route('/students')
def students_table():
    """Новая страница: табличный список студентов (задание дня 15)."""
    return render_template('students.html', students=students)


@app.route('/health')
def health():
    """Проверка работоспособности."""
    return {'status': 'ok', 'students_count': len(students)}


if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    print("=" * 50)
    print("Откройте браузер и перейдите по адресу:")
    print("http://localhost:5000")
    print("=" * 50)

    app.run(debug=False, host='127.0.0.1', port=5000)