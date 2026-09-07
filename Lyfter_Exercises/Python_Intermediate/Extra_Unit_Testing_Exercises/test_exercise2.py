import pytest


def divide(number1, number2):
    if isinstance(number1, str) or isinstance(number2, str):
        raise TypeError("Only numeric arguments are allowed")
    if number2 == 0:
        raise ValueError("You cannot divide by zero")
    return number1 / number2

#------------------ TESTS ------------------------->

def test_divide_returns_the_correct_result():
    number1 = 10
    number2 = 2

    result = divide(number1, number2)

    assert result == 5.0

def test_divide_throws_value_error_when_dividing_a_number_by_zero():
    number1 = 10
    number2 = 0

    with pytest.raises(ValueError, match="You cannot divide by zero"):
        divide(number1, number2)

def test_divide_throws_value_error_when_dividing_a_number_by_zero():
    number1 = 10
    number2 = 0

    with pytest.raises(ValueError, match="You cannot divide by zero"):
        divide(number1, number2)

def test_divide_throws_type_error_when_trying_to_divide_strings():
    number1 = "10"
    number2 = "25"

    with pytest.raises(TypeError):
        divide(number1, number2)