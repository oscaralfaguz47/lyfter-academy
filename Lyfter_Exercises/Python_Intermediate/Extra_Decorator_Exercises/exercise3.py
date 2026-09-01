from datetime import datetime
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result_of_the_function = func(*args, **kwargs)
        print(f"Func: {func.__name__} - args: {args[0]}, {args[1]} - [{datetime.today()}] - Result: {result_of_the_function:.2f}")
        print(F"Result: {result_of_the_function:.2f}")
        return result_of_the_function
    return wrapper

def validate_numbers(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in list(args):
            if not isinstance(arg, (int, float)):
                raise ValueError(f"The argument ({arg}) is not numeric")
        return func(*args, **kwargs)
    return wrapper

@log_call 
@validate_numbers
def multiply(num1, num2):
    return num1 * num2


list_of_numbers = [
    {
    "number1" : 80,
    "number2" : 75
    },
    {
    "number1" : 100,
    "number2" : "75"
    }
]

for number_to_multiply in list_of_numbers:
    try:
        result = multiply(number_to_multiply["number1"], number_to_multiply["number2"])
    except ValueError as e:
        print(e)