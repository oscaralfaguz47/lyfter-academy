import csv
from pathlib import Path

from menu.actions import Student

BASE_DIR = Path(__file__).resolve().parent
FILE_NAME = BASE_DIR / "students.csv"
FIELD_NAMES = [
    "full_name",
    "section",
    "spanish_score",
    "english_score",
    "social_studies_score",
    "sciences_score",
]


def export_data_to_csv(students_list, file_name=FILE_NAME):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(student.to_dict() for student in students_list)


def import_data_from_csv(file_name=FILE_NAME):
    with open(file_name, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [Student.from_dict(row) for row in reader]