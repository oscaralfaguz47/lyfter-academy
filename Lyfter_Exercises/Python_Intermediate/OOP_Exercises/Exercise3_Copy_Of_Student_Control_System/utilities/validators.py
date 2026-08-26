def ask_for_valid_number(subject, minNum, maxNum):
    while True:
        try:
            input_value = int(input(f"{subject}: "))
        except ValueError:
            print("Please enter a valid number.")
        else:
            if minNum <= input_value <= maxNum:
                return input_value
            print(f"The {subject} must be between {minNum} and {maxNum}")

def confirm_continue(subject):
    while True:
        input_value = input(f"{subject}: ")
        if input_value == "Y" or input_value == "y" or input_value == "N" or input_value == "n":
            if input_value == "Y" or input_value == "y":
                return True
            else:
                return False
        else:
            print("You must enter N or Y only")