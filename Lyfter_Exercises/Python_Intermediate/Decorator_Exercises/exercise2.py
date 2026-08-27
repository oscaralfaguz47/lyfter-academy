def validate_all_params_type_number(func):
    def wrapper(*args, **kwargs):
        for value in list(args) + list(kwargs.values()):
            if not isinstance(value, (int, float)):
                raise TypeError(f"The param ({value}) is not a number")
        print("All params are numeric")
        return func(*args, **kwargs)
    return wrapper

@validate_all_params_type_number
def sum_four_numbers(n1, n2, n3, n4):
    return n1 + n2 + n3 + n4


sum_four_numbers(50, 55, 2, 80)
try:
    sum_four_numbers(50, 55, "5", 80)
except TypeError as e:
    print(e)