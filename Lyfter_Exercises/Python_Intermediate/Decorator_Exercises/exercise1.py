def log_parameters_and_function(func):
    def wrapper(*args, **kwargs):
        print(f"Function Name: {func.__name__}")
        print(f" args: {args}")
        print(f" kwargs: {kwargs}")
        result_of_the_function = func(*args, **kwargs)
        print(f" return of the function: {result_of_the_function}")
        return result_of_the_function
    return wrapper

@log_parameters_and_function
def sum_three_numbers(number1, number2, number3):
    return number1 + number2 + number3

@log_parameters_and_function
def sum_two_numbers_and_multiply(number1, number2, multiply_by):
    return (number1 + number2) * multiply_by


sum_three_numbers(5, 10, 10)
sum_two_numbers_and_multiply(20, 20, multiply_by=2)