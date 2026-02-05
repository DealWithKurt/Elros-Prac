"""
Построение графиков.
"""

import matplotlib.pyplot as plt


def plot_subjects(subject_stats, filename):
    """
    График средних баллов по предметам.
    """
    if not subject_stats:
        return False

    subjects = list(subject_stats.keys())
    averages = [s['average'] for s in subject_stats.values()]

    sorted_pairs = sorted(zip(subjects, averages), key=lambda x: x[1], reverse=True)
    subjects, averages = zip(*sorted_pairs)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(subjects, averages, color='lightblue', edgecolor='black')

    plt.title('Средний балл по предметам', fontsize=14)
    plt.xlabel('Предметы')
    plt.ylabel('Средний балл')
    plt.ylim(2, 5)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)

    # Цифры на столбцах
    for bar, avg in zip(bars, averages):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
                 f'{avg:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    plt.close()

    return True


def plot_scores(score_counts, filename):
    """
    Гистограмма распределения оценок.
    """
    if not score_counts:
        return False

    scores = list(score_counts.keys())
    counts = list(score_counts.values())

    plt.figure(figsize=(8, 5))
    bars = plt.bar(scores, counts, color='lightgreen', edgecolor='black')

    plt.title('Распределение оценок', fontsize=14)
    plt.xlabel('Оценка')
    plt.ylabel('Количество')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Цифры на столбцах
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5,
                 str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    plt.close()

    return True


def plot_top_students(top_students, filename):
    """
    График топ-5 студентов.
    """
    if not top_students:
        return False

    students = [s for s, _ in top_students]
    averages = [a for _, a in top_students]

    plt.figure(figsize=(10, 5))
    bars = plt.barh(students, averages, color='lightcoral', edgecolor='black')

    plt.title('Топ-5 студентов', fontsize=14)
    plt.xlabel('Средний балл')
    plt.xlim(2, 5)
    plt.grid(axis='x', linestyle='--', alpha=0.7)

    # Цифры на столбцах
    for bar, avg in zip(bars, averages):
        width = bar.get_width()
        plt.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                 f'{avg:.2f}', ha='left', va='center')

    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    plt.close()

    return True