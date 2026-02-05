import csv
import matplotlib.pyplot as plt
import statistics
from collections import defaultdict
from pathlib import Path


def load_csv_data(file_path):
    """
    Загружает данные из CSV файла.
    """
    data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                if len(row) < 3:
                    continue

                name = row[0].strip()
                subject = row[1].strip()
                score_str = row[2].strip()

                if not name or not subject or not score_str:
                    continue

                try:
                    score = float(score_str)
                    if 2 <= score <= 5:
                        data.append({
                            'name': name,
                            'subject': subject,
                            'score': score
                        })
                except ValueError:
                    continue

        print(f"Загружено записей: {len(data)}")
        return data

    except FileNotFoundError:
        print(f"Ошибка: файл не найден - {file_path}")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def calculate_subject_averages(data):
    """
    Рассчитывает средние баллы по предметам.
    """
    subject_scores = defaultdict(list)

    for record in data:
        subject_scores[record['subject']].append(record['score'])

    subject_stats = {}
    for subject, scores in subject_scores.items():
        subject_stats[subject] = {
            'average': statistics.mean(scores),
            'count': len(scores),
            'min': min(scores),
            'max': max(scores)
        }

    return subject_stats


def create_bar_chart(subject_stats, output_path):
    """
    Создает столбчатую диаграмму средних баллов по предметам.
    """
    subjects = list(subject_stats.keys())
    averages = [subject_stats[s]['average'] for s in subjects]
    counts = [subject_stats[s]['count'] for s in subjects]

    sorted_data = sorted(zip(subjects, averages, counts),
                         key=lambda x: x[1],
                         reverse=True)
    subjects, averages, counts = zip(*sorted_data)

    plt.figure(figsize=(12, 6))

    bars = plt.bar(subjects, averages, color='skyblue', edgecolor='black')

    for bar, avg, count in zip(bars, averages, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 0.02,
                 f'{avg:.2f}\n({count})',
                 ha='center', va='bottom', fontsize=9)

    plt.title('Средний балл по предметам', fontsize=16, fontweight='bold')
    plt.xlabel('Предметы', fontsize=12)
    plt.ylabel('Средний балл', fontsize=12)
    plt.ylim(2, 5)  # Диапазон оценок
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')

    overall_avg = statistics.mean(averages)
    plt.axhline(y=overall_avg, color='red', linestyle='--',
                linewidth=2, alpha=0.7, label=f'Общее среднее: {overall_avg:.2f}')
    plt.legend()

    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Столбчатая диаграмма сохранена: {output_path}")

    plt.show()


def create_histogram(data, output_path):
    """
    Создает гистограмму распределения оценок.
    """
    all_scores = [record['score'] for record in data]

    plt.figure(figsize=(10, 6))

    n, bins, patches = plt.hist(all_scores, bins=15, color='lightgreen',
                                edgecolor='black', alpha=0.7)

    plt.title('Распределение оценок студентов', fontsize=16, fontweight='bold')
    plt.xlabel('Оценка', fontsize=12)
    plt.ylabel('Количество оценок', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    mean_score = statistics.mean(all_scores)
    plt.axvline(x=mean_score, color='red', linestyle='--',
                linewidth=2, alpha=0.7, label=f'Среднее: {mean_score:.2f}')

    stats_text = f'''Всего оценок: {len(all_scores)}
Минимум: {min(all_scores):.1f}
Максимум: {max(all_scores):.1f}
Среднее: {mean_score:.2f}'''

    plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.legend()

    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Гистограмма сохранена: {output_path}")

    plt.show()


def create_comparison_chart(subject_stats, output_path):
    """
    Дополнительный график: сравнение предметов.
    """
    subjects = list(subject_stats.keys())
    averages = [subject_stats[s]['average'] for s in subjects]
    counts = [subject_stats[s]['count'] for s in subjects]

    sorted_data = sorted(zip(subjects, averages, counts),
                         key=lambda x: x[1],
                         reverse=True)
    subjects, averages, counts = zip(*sorted_data)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    bars1 = ax1.bar(subjects, averages, color='lightcoral', edgecolor='black')
    ax1.set_title('Средний балл по предметам', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Средний балл', fontsize=12)
    ax1.set_ylim(2, 5)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.set_xticklabels(subjects, rotation=45, ha='right')

    for bar, avg in zip(bars1, averages):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.02,
                 f'{avg:.2f}', ha='center', va='bottom', fontsize=9)

    bars2 = ax2.bar(subjects, counts, color='lightblue', edgecolor='black')
    ax2.set_title('Количество оценок по предметам', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Количество оценок', fontsize=12)
    ax2.set_xlabel('Предметы', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    ax2.set_xticklabels(subjects, rotation=45, ha='right')

    for bar, count in zip(bars2, counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 str(count), ha='center', va='bottom', fontsize=9)

    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Сравнительный график сохранен: {output_path}")

    plt.show()


def main():
    """
    Основная функция.
    """
    input_file = "data/students_scores.csv"

    print("=" * 50)
    print("Визуализация данных оценок студентов")
    print("=" * 50)

    if not Path(input_file).exists():
        print(f"Файл {input_file} не найден.")
        print("Сначала скопируйте файл из day08/data/ или создайте тестовые данные.")
        print("Пример: cp ../day08/data/students_scores.csv data/")
        return 1

    data = load_csv_data(input_file)
    if not data:
        print("Нет данных для визуализации")
        return 1

    subject_stats = calculate_subject_averages(data)

    print("\nСтатистика по предметам:")
    print("-" * 40)
    for subject, stats in sorted(subject_stats.items()):
        print(f"{subject}: {stats['average']:.2f} (оценок: {stats['count']})")

    print("\nСоздание графиков...")

    bar_chart_path = "figures/avg_by_subject.png"
    create_bar_chart(subject_stats, bar_chart_path)

    histogram_path = "figures/grades_hist.png"
    create_histogram(data, histogram_path)

    comparison_path = "figures/subject_comparison.png"
    create_comparison_chart(subject_stats, comparison_path)

    print("\n" + "=" * 50)
    print("Визуализация завершена успешно!")
    print(f"Графики сохранены в папке: figures/")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)