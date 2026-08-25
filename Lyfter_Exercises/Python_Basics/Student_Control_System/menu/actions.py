from utilities.validators import ask_for_valid_number, confirm_continue

def enter_students_info(students_list):
    print("# You are about to enter new student's info ---")

    while True:
        full_name = input("Enter the student's full name: ")
        section = input("Enter the section (Ex: 11B): ")
        spanish_grade = ask_for_valid_number("Enter the Spanish grade", 1, 100)
        english_grade = ask_for_valid_number("Enter the English grade", 1, 100)
        social_studies_grade = ask_for_valid_number("Enter the Social Studies grade", 1, 100)
        science_grade = ask_for_valid_number("Enter the Science grade", 1, 100)

        students_list.append({
            "full_name": full_name,
            "section" : section,
            "spanish_grade" : spanish_grade,
            "english_grade" : english_grade,
            "social_studies_grade" : social_studies_grade,
            "science_grade" : science_grade
        })

        if not confirm_continue("Do you want to add another student?, press Y/N to continue"):
            return students_list



def view_students_info(students_list):
    if not students_list:
        enter_students_confirm = confirm_continue("There aren't students added yet, do you want to add new?, Y/N")
        if enter_students_confirm:
            students_list = enter_students_info(students_list)
        print("# EXISTING STUDENTS ---")
    for student in students_list:
        print(f"{student['full_name']} ({student['section']})")
        print(f"  Spanish: {student['spanish_grade']}")
        print(f"  English: {student['english_grade']}")
        print(f"  Social Studies: {student['social_studies_grade']}")
        print(f"  Science: {student['science_grade']}")
        print()
    return students_list
        

GRADE_KEYS = ["spanish_grade", "english_grade", "social_studies_grade", "science_grade"]

def get_average(student):
    return sum(student[key] for key in GRADE_KEYS) / len(GRADE_KEYS)

def view_top3_highest_grade_average(students_list):
    if not students_list:
        print("There are no students yet.")
        return

    top_students = sorted(students_list, key=get_average, reverse=True)[:3]

    print("# TOP 3 HIGHEST GRADE AVERAGE ---")
    for position, student in enumerate(top_students, start=1):
        print(f"{position}. {student['full_name']} ({student['section']}) - {get_average(student):.2f}")


def view_overall_average(students_list):
    if not students_list:
        print("There are no students yet.")
        return

    averages = [get_average(student) for student in students_list]
    overall_average = sum(averages) / len(averages)

    print("# OVERALL AVERAGE ---")
    print(f"Students: {len(students_list)}")
    print(f"Overall average: {overall_average:.2f}")