def repeat_twice(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper


@repeat_twice
def print_hello_name(name):
    print(f"Hello, [{name}]")

print_hello_name("Oscar")