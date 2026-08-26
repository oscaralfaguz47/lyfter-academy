from utilities.validators import ask_for_valid_number
from menu.actions import enter_students_info, view_overall_average, view_top3_highest_score_average, view_students_info
from data.data import import_data_from_csv, export_data_to_csv
from utilities.validators import confirm_continue

def run_menu():
    students_list = []

    print("----- WELCOME TO THE STUDENT MANAGEMENT SYSTEM -----")
    while True:
        print("Enter a number from the menu below: ")
        print("1. Enter student information.")
        print("2. View student's information.")
        print("3. View top 3 highest score average.")
        print("4. View overall average across all students.")
        print("5. Export all data to a CSV file.")
        print("6. Import data from a CSV file.")
        print("7. Exit.")

        menu_option = ask_for_valid_number("", 1, 7)

        if menu_option == 1:
            students_list = enter_students_info(students_list)
        elif menu_option == 2:
            students_list = view_students_info(students_list)
        elif menu_option == 3:
            view_top3_highest_score_average(students_list)
        elif menu_option == 4:
            view_overall_average(students_list)
        elif menu_option == 5:
            if not students_list:
                print("There are no students to export.")
            else:
                export_data_to_csv(students_list)
                print(f"{len(students_list)} students exported successfully.")
        elif menu_option == 6:
            try:
                students_list = import_data_from_csv()
            except FileNotFoundError:
                print("There is no exported file yet. Export your data first.")
            else:
                print(f"{len(students_list)} students imported successfully.")
        elif menu_option == 7:
            print("Goodbye!")
            break

        if not confirm_continue("Enter Y to continue in the menu or N to exit."):
            break
