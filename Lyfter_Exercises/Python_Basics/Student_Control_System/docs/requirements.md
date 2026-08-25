# Student Management System 

## Requirements 

You must create a program with a command-line interface (that is, based on `inputs` and `prints`). It must have a menu that provides access to all the features:

1. It must validate that a valid menu option is entered. ✅
2. Enter information for `n` number of students, one at a time. Each student must include: ✅
   * Full name
   * Section (example: `11B`)
   * Spanish grade
   * English grade
   * Social Studies grade
   * Science grade
3. It must validate that the grades entered are valid (numbers from 0 to 100) and keep asking for them until they are valid. ✅
4. View the information of all entered students. ✅
5. View the top 3 students with the highest grade average (that is, the average of `Spanish grade` + `English grade` + `Social Studies grade` + `Science grade`). ✅
6. View the overall average across all students' grades (that is, the average of each student's `grade average`). ✅
7. Export all current data to a `CSV` file. ✅
8. Import data from a previously exported `CSV` file. If there is no previously exported file, it must inform the user. ✅

## Project Structure 

You must split the project into the following modules:

* `main`: will contain the program's entry point.
* `menu`: will contain all the logic related to the options menu.
* `actions`: will contain all the logic for the menu actions, except for exporting and importing data.
* `data`: will contain all the data export and import logic.

## Extra Requirements (Optional) 

1. Add a new menu option that allows deleting a student using their name and section. It must validate:
   * Whether the student exists or not.
   * Confirm with the user before deleting.
2. Display failing students, listing all those who have at least one subject with a grade below 60.
   * Add a menu option: `View failing students`.
   * Display the name, section, and the failed subjects along with their grades.
3. Improve the system by adding the following error handling:
   * That the full name is neither empty nor contains numbers.
   * That the section follows a valid format (example: `10A`, `11B`, etc.).
   * That two students with the same name and section cannot be entered (no duplicates).
   * Tip: You can create the functions `is_valid_name`, `is_valid_section`, and `student_exists`.


