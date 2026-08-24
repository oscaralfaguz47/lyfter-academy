print("----- My calculator -----")

global_current_number = 10
class InvalidOperatorError(Exception):
    def __init__(self, message="Operator not valid. Use +, -, * or /"):
        super().__init__(message)

def calculate(current_number, new_number, operation):
    if (operation == "+"):
        return current_number + new_number
    elif (operation == "-"):
        return current_number - new_number
    elif (operation == "/"):
        if new_number == 0:
            raise ZeroDivisionError("You cannot divide by zero")
        return current_number / new_number
    elif (operation == "*"):
        return current_number * new_number
    else:
        raise InvalidOperatorError()


def initialize_calculator(current_number):
    operator = input("Insert +, -, * or /: ")

    try:
        new_number = float(input("Insert a number: "))
        result = calculate(current_number, new_number, operator)
    except InvalidOperatorError as e:
        print(f"Error: {e}")
    except ZeroDivisionError as e:
        print("Error: {e}")
    except ValueError:
        print("Error: that's not a valid number")
    else:
        print(f"The result of {current_number} {operator} {new_number} is equals to: {result}")
        global_current_number = result
        print(f"Now the value of the global current number is: {global_current_number}")
        confirm_initialize_calculator = input("Do you want to initialize the calculator?, press Y/N: ")
        try:
            if confirm_initialize_calculator == "Y" or confirm_initialize_calculator == "y":
                initialize_calculator(global_current_number)
            elif confirm_initialize_calculator != "Y" and confirm_initialize_calculator != "y" and confirm_initialize_calculator != "N" and confirm_initialize_calculator != "n":
                raise ValueError("Invalid value, you must enter Y or N only")
            else:
                print("Thanks for using the calculator!")
        except ValueError as e:
            print(f"Error: {e}")

initialize_calculator(global_current_number)
