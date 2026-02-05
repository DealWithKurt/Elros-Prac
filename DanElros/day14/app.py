from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import uuid
import sys

app = Flask(__name__)
app.secret_key = 'секретный-ключ-для-flask'

students = [
    {
        'id': 1,
        'name': 'Иванов Иван',
        'age': 20,
        'created_at': datetime.now()
    },
    {
        'id': 2,
        'name': 'Петрова Анна',
        'age': 21,
        'created_at': datetime.now()
    },
    {
        'id': 3,
        'name': 'Сидоров Сергей',
        'age': 19,
        'created_at': datetime.now()
    }
]


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
            'id': str(uuid.uuid4()),
            'name': name,
            'age': age_int,
            'created_at': datetime.now()
        }

        students.append(new_student)
        flash(f'Студент {name} успешно добавлен!', 'success')
        return redirect(url_for('index'))

    return render_template('add.html', students=students)


@app.route('/health')
def health():
    """Проверка работоспособности."""
    return {'status': 'ok', 'students_count': len(students)}


if __name__ == '__main__':
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    print("=" * 50)
    print("Flask приложение запущено")
    print("Откройте браузер и перейдите по адресу:")
    print("http://localhost:5000")
    print("=" * 50)

    app.run(debug=False, host='127.0.0.1', port=5000)