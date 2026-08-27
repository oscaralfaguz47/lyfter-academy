print("----- Greeting -----")

def enter_name():
    user_name = input("Enter your name: ")
    if user_name.isdigit():
        raise ValueError("The name cannot be numeric")
    return user_name

def enter_age():
    try:
        return int(input("Enter your age: "))
    except ValueError:
        raise ValueError("Not valid number, enter numeric only")


def print_result(user_name, user_age):
    print(f"Hello {user_name}, your age is {user_age}")

try:
    user_name = enter_name()
    user_age = enter_age()
    print_result(user_name, user_age)
except ValueError as e:
    print({e})


