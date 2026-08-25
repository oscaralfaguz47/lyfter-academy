import csv

FILE_NAME = "students.csv"
FIELD_NAMES = [
    "full_name",
    "section",
    "spanish_grade",
    "english_grade",
    "social_studies_grade",
    "science_grade",
]
GRADE_KEYS = FIELD_NAMES[2:]


def export_data_to_csv(students_list, file_name=FILE_NAME):
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(students_list)


def import_data_from_csv(file_name=FILE_NAME):
    students_list = []
    with open(file_name, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = dict(row)
            for key in GRADE_KEYS:
                student[key] = int(student[key])
            students_list.append(student)
    return students_list