from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import re
import csv
from io import StringIO
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'секретный-ключ-для-flask'

DATA_FILE = Path("data/students.json")


def validate_name(name):
    if not name or not name.strip():
        return False, "Имя не может быть пустым"

    name = name.strip()

    if not re.match(r'^[А-Яа-яA-Za-z\s]+$', name):
        return False, "Имя может содержать только буквы и пробелы"

    if len(name) < 2:
        return False, "Имя слишком короткое"
    if len(name) > 50:
        return False, "Имя слишком длинное"

    return True, name


def validate_age(age_str):
    if not age_str:
        return False, "Возраст не может быть пустым"

    try:
        age = int(age_str)
        if age < 16:
            return False, "Возраст должен быть не менее 16 лет"
        if age > 35:
            return False, "Возраст должен быть не более 35 лет"
        return True, age
    except ValueError:
        return False, "Возраст должен быть числом"


def validate_group(group):
    if not group:
        return True, ""

    group = group.strip()
    if len(group) > 20:
        return False, "Название группы слишком длинное"

    return True, group


def load_students():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for student in data:
                    if isinstance(student.get('created_at'), str):
                        student['created_at'] = datetime.fromisoformat(student['created_at'])
                    if isinstance(student.get('updated_at'), str):
                        student['updated_at'] = datetime.fromisoformat(student['updated_at'])
                return data
        except Exception:
            return []
    else:
        return []


def save_students(students_list):
    try:
        data_to_save = []
        for student in students_list:
            student_copy = student.copy()
            if isinstance(student_copy.get('created_at'), datetime):
                student_copy['created_at'] = student_copy['created_at'].isoformat()
            if isinstance(student_copy.get('updated_at'), datetime):
                student_copy['updated_at'] = student_copy['updated_at'].isoformat()
            data_to_save.append(student_copy)

        DATA_FILE.parent.mkdir(exist_ok=True)

        temp_file = DATA_FILE.with_suffix('.tmp')
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

        temp_file.replace(DATA_FILE)
        return True
    except Exception:
        return False


def get_next_id(students_list):
    if not students_list:
        return 1

    max_id = 0
    for student in students_list:
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


def find_student_by_id(students_list, student_id):
    for student in students_list:
        if str(student.get('id')) == str(student_id):
            return student
    return None


def load_data():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(exist_ok=True, parents=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    return load_students()


def export_to_csv(students_list):
    output = StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow(['ID', 'Имя', 'Возраст', 'Группа', 'Дата добавления', 'Дата обновления'])

    for student in students_list:
        writer.writerow([
            student['id'],
            student['name'],
            student['age'],
            student.get('group', ''),
            student['created_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(student['created_at'], datetime) else
            student['created_at'],
            student['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(student['updated_at'], datetime) else
            student['updated_at']
        ])

    return output.getvalue()


def create_export_folder():
    export_folder = Path("exports")
    export_folder.mkdir(exist_ok=True)
    return export_folder


@app.route('/')
def index():
    students_list = load_data()
    search_query = request.args.get('search', '').strip()
    group_filter = request.args.get('group', '').strip()

    filtered_students = students_list

    if search_query:
        filtered_students = [
            student for student in filtered_students
            if search_query.lower() in student['name'].lower()
        ]

    if group_filter:
        filtered_students = [
            student for student in filtered_students
            if student.get('group') == group_filter
        ]

    all_groups = sorted(list(set(
        student['group'] for student in students_list
        if student.get('group')
    )))

    return render_template('index.html',
                           students=filtered_students,
                           all_groups=all_groups,
                           search_query=search_query,
                           selected_group=group_filter)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    students_list = load_data()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        group = request.form.get('group', '').strip()

        name_valid, name_message = validate_name(name)
        age_valid, age_message = validate_age(age)
        group_valid, group_message = validate_group(group)

        errors = []

        if not name_valid:
            errors.append(name_message)
        if not age_valid:
            errors.append(age_message)
        if not group_valid:
            errors.append(group_message)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add.html')

        new_student = {
            'id': get_next_id(students_list),
            'name': name_message,
            'age': age_message,
            'group': group_message,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        students_list.append(new_student)

        if save_students(students_list):
            flash(f'Студент "{name_message}" успешно добавлен!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Ошибка при сохранении данных', 'error')
            return render_template('add.html')

    return render_template('add.html')


@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    students_list = load_data()
    student = find_student_by_id(students_list, student_id)

    if not student:
        flash(f'Студент с ID {student_id} не найден', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        group = request.form.get('group', '').strip()

        name_valid, name_message = validate_name(name)
        age_valid, age_message = validate_age(age)
        group_valid, group_message = validate_group(group)

        errors = []

        if not name_valid:
            errors.append(name_message)
        if not age_valid:
            errors.append(age_message)
        if not group_valid:
            errors.append(group_message)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit.html', student=student)

        student['name'] = name_message
        student['age'] = age_message
        student['group'] = group_message
        student['updated_at'] = datetime.now()

        if save_students(students_list):
            flash(f'Данные студента "{name_message}" успешно обновлены!', 'success')
            return redirect(url_for('index'))
        else:
            flash(f'Ошибка при сохранении данных', 'error')
            return render_template('edit.html', student=student)

    return render_template('edit.html', student=student)


@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    students_list = load_data()
    student = find_student_by_id(students_list, student_id)

    if not student:
        flash(f'Студент с ID {student_id} не найден', 'error')
        return redirect(url_for('index'))

    student_name = student['name']
    students_list.remove(student)

    if save_students(students_list):
        flash(f'Студент "{student_name}" успешно удален!', 'success')
    else:
        flash(f'Ошибка при сохранении данных', 'error')

    return redirect(url_for('index'))


@app.route('/students')
def students_table():
    students_list = load_data()
    search_query = request.args.get('search', '').strip()
    group_filter = request.args.get('group', '').strip()

    filtered_students = students_list

    if search_query:
        filtered_students = [
            student for student in filtered_students
            if search_query.lower() in student['name'].lower()
        ]

    if group_filter:
        filtered_students = [
            student for student in filtered_students
            if student.get('group') == group_filter
        ]

    all_groups = sorted(list(set(
        student['group'] for student in students_list
        if student.get('group')
    )))

    return render_template('students.html',
                           students=filtered_students,
                           all_groups=all_groups,
                           search_query=search_query,
                           selected_group=group_filter)


@app.route('/export/csv')
def export_csv():
    students_list = load_data()

    if not students_list:
        flash('Нет данных для экспорта', 'error')
        return redirect(url_for('index'))

    csv_data = export_to_csv(students_list)

    export_folder = create_export_folder()
    filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = export_folder / filename

    try:
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(csv_data)

        flash(f'Данные экспортированы в файл: {filename}', 'success')
    except Exception as e:
        flash(f'Ошибка при экспорте данных: {str(e)}', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8585)