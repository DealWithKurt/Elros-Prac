import statistics
from collections import defaultdict


def analyze_data(data):
    """
    Анализирует данные, возвращает статистику.
    """
    if not data:
        return {}

    student_scores = defaultdict(list)
    subject_scores = defaultdict(list)
    all_scores = []

    for record in data:
        student = record['student']
        subject = record['subject']
        score = record['score']

        student_scores[student].append(score)
        subject_scores[subject].append(score)
        all_scores.append(score)

    student_stats = {}
    for student, scores in student_scores.items():
        student_stats[student] = {
            'average': statistics.mean(scores),
            'count': len(scores)
        }

    top_students = sorted(
        [(s, stats['average']) for s, stats in student_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    subject_stats = {}
    for subject, scores in subject_scores.items():
        subject_stats[subject] = {
            'average': statistics.mean(scores),
            'count': len(scores),
            'min': min(scores),
            'max': max(scores)
        }

    overall_stats = {
        'total': len(data),
        'students': len(student_scores),
        'subjects': len(subject_scores),
        'avg_all': statistics.mean(all_scores),
        'min_all': min(all_scores),
        'max_all': max(all_scores)
    }

    score_counts = {}
    for score in all_scores:
        score_int = int(score)
        score_counts[score_int] = score_counts.get(score_int, 0) + 1

    return {
        'overall': overall_stats,
        'students': student_stats,
        'subjects': subject_stats,
        'top_students': top_students,
        'score_counts': score_counts
    }


def create_report(analysis):
    """
    Создает текстовый отчет.
    """
    if not analysis:
        return "Нет данных"

    report = []
    report.append("=" * 50)
    report.append("ОТЧЕТ ПО СТУДЕНТАМ")
    report.append("=" * 50)

    o = analysis['overall']
    report.append(f"\nОбщая статистика:")
    report.append(f"  Всего записей: {o['total']}")
    report.append(f"  Студентов: {o['students']}")
    report.append(f"  Предметов: {o['subjects']}")
    report.append(f"  Средний балл: {o['avg_all']:.2f}")
    report.append(f"  Диапазон: {o['min_all']:.1f}-{o['max_all']:.1f}")
    report.append(f"\nТоп-5 студентов:")

    for i, (student, avg) in enumerate(analysis['top_students'], 1):
        report.append(f"  {i}. {student}: {avg:.2f}")

    report.append(f"\nСредние баллы по предметам:")
    for subject, stats in sorted(analysis['subjects'].items()):
        report.append(f"  {subject}: {stats['average']:.2f} (оценок: {stats['count']})")

    report.append(f"\nРаспределение оценок:")
    for score in sorted(analysis['score_counts'].keys()):
        count = analysis['score_counts'][score]
        report.append(f"  Оценка {score}: {count}")

    report.append("\n" + "=" * 50)

    return "\n".join(report)