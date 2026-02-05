from .math_utils import (
    add,
    sub,
    mul,
    div,
    is_prime,
    calculate_statistics
)

from .student_utils import (
    avg_grade,
    sort_by_age,
    best_students,
    unique_names
)

from .file_utils import (
    read_numbers_from_file,
    save_with_atomic_write,
    load_json_file,
    save_json_file
)

__all__ = [
    'add',
    'sub',
    'mul',
    'div',
    'is_prime',
    'calculate_statistics',

    'avg_grade',
    'sort_by_age',
    'best_students',
    'unique_names',

    'read_numbers_from_file',
    'save_with_atomic_write',
    'load_json_file',
    'save_json_file',
]

__version__ = '1.0.0'