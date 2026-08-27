from utilities.validators import ask_for_valid_number, confirm_continue

class Student():
    def __init__(self, full_name, section, spanish_score, english_score, social_studies_score, sciences_score):
        self.full_name = full_name
        self.section = section
        self.spanish_score = spanish_score
        self.english_score = english_score
        self.social_studies_score = social_studies_score
        self.sciences_score = sciences_score

    def get_scores(self):
        return [self.spanish_score, self.english_score, self.social_studies_score, self.sciences_score]

    def get_average(self):
        scores = self.get_scores()
        return sum(scores) / len(scores)
    
    def to_dict(self):
        return {
            "full_name" : self.full_name,
            "section" : self.section,
            "spanish_score" : self.spanish_score,
            "english_score" : self.english_score,
            "social_studies_score" : self.social_studies_score,
            "sciences_score" : self.sciences_score
        }
    @classmethod
    def from_dict(cls, row):
        return cls(
            full_name=row["full_name"],
            section=row["section"],
            spanish_score=int(row["spanish_score"]),
            english_score=int(row["english_score"]),
            social_studies_score=int(row["social_studies_score"]),
            sciences_score=int(row["sciences_score"])
        )

    

def enter_students_info(students_list):
    print("# You are about to enter new student's info ---")

    while True:
        full_name = input("Enter the student's full name: ")
        section = input("Enter the section (Ex: 11B): ")
        spanish_score = ask_for_valid_number("Enter the Spanish score", 1, 100)
        english_score = ask_for_valid_number("Enter the English score", 1, 100)
        social_studies_score = ask_for_valid_number("Enter the Social Studies score", 1, 100)
        sciences_score = ask_for_valid_number("Enter the sciences score", 1, 100)

        students_list.append(
            Student(full_name, section, spanish_score, english_score, social_studies_score, sciences_score)
        )

        if not confirm_continue("Do you want to add another student?, press Y/N to continue"):
            return students_list



def view_students_info(students_list):
    if not students_list:
        enter_students_confirm = confirm_continue("There aren't students added yet, do you want to add new?, Y/N")
        if enter_students_confirm:
            students_list = enter_students_info(students_list)
        print("# EXISTING STUDENTS ---")
    for student in students_list:
        print(f"{student.full_name} ({student.section})")
        print(f"  Spanish: {student.spanish_score}")
        print(f"  English: {student.english_score}")
        print(f"  Social Studies: {student.social_studies_score}")
        print(f"  sciences: {student.sciences_score}")
        print()
    return students_list
        


def view_top3_highest_score_average(students_list):
    if not students_list:
        print("There are no students yet.")
        return

    top_students = sorted(students_list, key=Student.get_average, reverse=True)[:3]

    print("# TOP 3 HIGHEST SCORES AVERAGE ---")
    for position, student in enumerate(top_students, start=1):
        print(f"{position}. {student.full_name} ({student.section}) - {student.get_average():.2f}")


def view_overall_average(students_list):
    if not students_list:
        print("There are no students yet.")
        return

    averages = [student.get_average() for student in students_list]
    overall_average = sum(averages) / len(averages)

    print("# OVERALL AVERAGE ---")
    print(f"Students: {len(students_list)}")
    print(f"Overall average: {overall_average:.2f}")