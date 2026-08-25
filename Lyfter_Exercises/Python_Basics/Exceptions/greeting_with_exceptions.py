print("----- Greeting -----")

try:
    user_name = input("Enter your name: ")
    if user_name.isdigit():
        raise ValueError("The name cannot be numeric")
    user_age = input("Enter your age: ")
    if not user_age.isdigit():
        raise ValueError("Not valid number, enter numeric only")
    print(f"Hello {user_name}, your age is {user_age}")
except ValueError as e:
    print(f"Error: {e}")







# Ask the name to the user, if the name is numeric do raise ValueError("The name cannot be numeric")
# Ask the age to the user, if it's not a valid number, capture the ValueError and show the validation message