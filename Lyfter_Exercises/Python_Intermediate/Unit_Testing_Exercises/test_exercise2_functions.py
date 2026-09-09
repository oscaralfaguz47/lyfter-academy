import pytest
from exercise2_functions import sum_numbers_in_list, reverse_string, print_upper_and_lower_num_in_string, order_words_in_a_string, return_prime_numbers

# FUNCTION: sum_numbers_in_list  -----------------------------------------------
def test_sum_numbers_in_list_verify_function_sums_the_numbers():
    # Arrange
    my_list_of_numbers = [50, 50, 100]
    # Act
    total_sum = sum_numbers_in_list(my_list_of_numbers)
    # Assert
    assert total_sum == 200

def test_sum_numbers_in_list_verify_only_numbers_are_accepted():
    # Arrange
    my_list_of_numbers = [50, 50, 100, "Oscar"]
    # Act & Assert
    with pytest.raises(TypeError):
        sum_numbers_in_list(my_list_of_numbers)

def test_sum_numbers_in_list_verify_that_an_empty_list_is_not_allow():
    # Arrange
    my_list_of_numbers = []
    # Act & Assert
    with pytest.raises(ValueError):
        sum_numbers_in_list(my_list_of_numbers)
    


# FUNCTION: reverse_string -----------------------------------------------
def test_reverse_string_verify_function_reverses_a_string():
    # Arrange 
    string_to_reverse = "Im learning Python"
    # Act
    result = reverse_string(string_to_reverse)
    # Assert
    assert result == "nohtyP gninrael mI"

def test_reverse_string_verify_the_correct_validation_message_is_displayed_when_a_non_string_is_giving_as_parameter():
    # Arrange 
    string_to_reverse = 45
    # Act & Assert
    with pytest.raises(TypeError, match=f"The parameter '{string_to_reverse} is not a string"):
        reverse_string(string_to_reverse)

def test_reverse_string_verify_validation_message_is_displayed_for_character_limit_of_80():
    # Arrange 
    string_to_reverse = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem1"
    print(len(string_to_reverse))
    # Act & Assert
    with pytest.raises(ValueError, match=f"The character limit is 80, you entered {len(string_to_reverse)}"):
        reverse_string(string_to_reverse)


# FUNCTION: print_upper_and_lower_num_in_string -----------------------------------------------
def test_print_upper_and_lower_num_in_string_verify_the_correct_message_is_printed(capsys):
    # Arrange
    my_string = "Hello World In Python by Oscar"
    # Act
    print_upper_and_lower_num_in_string(my_string)
    capture = capsys.readouterr()
    # Assert
    assert "He have 5 upper cases and 20 cases." in capture.out

def test_print_upper_and_lower_num_in_string_verify_the_string_does_not_allow_numeric_chars():
    # Arrange
    my_string = "Hello World 3"
    # Act & Assert
    with pytest.raises(TypeError):
        print_upper_and_lower_num_in_string(my_string)

def test_print_upper_and_lower_num_in_string_verify_that_the_parameter_cannot_be_an_empty_string_or_null(capsys):
    # Arrange
    my_string1 = ""
    my_string2 = None
    # Act & Assert
    with pytest.raises(ValueError):
        print_upper_and_lower_num_in_string(my_string1)
    with pytest.raises(ValueError):
        print_upper_and_lower_num_in_string(my_string2)

# FUNCTION: order_words_in_a_string -----------------------------------------------
def test_order_words_in_a_string_verify_that_the_function_orders_words_in_a_string():
    # Arrange
    my_string_to_order = "pizza-chair-computer-hair-mouse-yourself"
    # Act
    ordered_string = order_words_in_a_string(my_string_to_order)
    # Assert
    assert ordered_string == "chair-computer-hair-mouse-pizza-yourself"

def test_order_words_in_a_string_verify_a_validation_message_is_displayed_if_the_string_has_more_than_6_words():
    # Arrange
    my_string_to_order = "pizza-chair-computer-hair-mouse-yourself-té"
    # Act & Assert
    with pytest.raises(ValueError, match="The list cannot contain more that 6 words"):
        order_words_in_a_string(my_string_to_order)

def test_order_words_in_a_string_verify_that_a_validation_message_is_displayed_if_the_string_has_spaces():
    # Arrange
    my_string_to_order = "pizza-chair-computer-hair-mouse yourself"
    # Act & Assert
    with pytest.raises(ValueError, match="The string cannot contains spaces"):
        order_words_in_a_string(my_string_to_order)

# FUNCTION: return_prime_numbers -----------------------------------------------
def test_return_prime_numbers_verify_that_the_function_return_only_prime_numbers():
    # Arrange
    list_of_numbers = [1, 6, 13, 7, 5, 8, 2, -1]
    # Act
    list_of_prime_numbers = return_prime_numbers(list_of_numbers)
    # Assert
    assert list_of_prime_numbers == [13, 7, 5, 2]

def test_return_prime_numbers_verify_that_if_there_are_no_prime_numbers_return_empty_list():
    # Arrange
    list_of_numbers = [1, 6, 8, -1, 80, -10]
    # Act
    list_of_prime_numbers = return_prime_numbers(list_of_numbers)
    # Assert
    assert list_of_prime_numbers == []

def test_return_prime_numbers_verify_that_validation_messages_are_displayed_for_none_and_empty_lists_as_arguments():
    # Arrange
    empty_list = []
    list_as_none = None
    # Act & Assert
    with pytest.raises(ValueError, match="The list cannot be empty"):
        return_prime_numbers(empty_list)
    with pytest.raises(TypeError, match="The list cannot be None"):
        return_prime_numbers(list_as_none)
