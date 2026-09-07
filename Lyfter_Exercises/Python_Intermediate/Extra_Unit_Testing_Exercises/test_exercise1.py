import pytest

def sum_two_numbers(num1, num2):    
    return num1 + num2

class TestNumbers:

    def test_sum_numbers_sums_positive_numbers(self):
            number1 = 150
            number2 = 200
    
            result = sum_two_numbers(number1, number2)
    
            assert result == 350

    def test_sum_numbers_sums_negative_numbers(self):
        number1 = -150
        number2 = -200

        result = sum_two_numbers(number1, number2)

        assert result == -350

    def test_sum_numbers_sums_numbers_with_zeros(self):
            number1 = 0
            number2 = 0
    
            result = sum_two_numbers(number1, number2)
    
            assert result == 0