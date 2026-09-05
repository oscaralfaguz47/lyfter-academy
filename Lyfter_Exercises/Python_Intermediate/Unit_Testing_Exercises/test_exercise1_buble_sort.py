import random
import pytest
from exercise1_bubble_sort import bubble_sort


def test_bubble_sort_Verify_bubble_sort_function_works_with_small_list():
    # Arrange
    my_unordered_list = [100, 50, -10, 70, 2, 15, 1]

    # Act
    ordered_list = bubble_sort(my_unordered_list)

    # Assert
    assert ordered_list == [-10, 1, 2, 15, 50, 70, 100]

def test_bubble_sort_Verify_bubble_sort_function_works_with_large_list():
    # Arrange
    my_ordered_list_to_compare = list(range(10000))
    my_shuffle_list = random.sample(my_ordered_list_to_compare, len(my_ordered_list_to_compare))

    # Act
    ordered_list = bubble_sort(my_shuffle_list)

    # Assert
    assert ordered_list == my_ordered_list_to_compare

def test_bubble_sort_Verify_bubble_sort_function_works_with_empty_list():
    # Arrange
    my_empty_list = []

    # Act
    ordered_list = bubble_sort(my_empty_list)

    # Assert
    assert ordered_list == []

def test_bubble_sort_Verify_bubble_sort_function_works_with_no_list_type_as_parameter():
    # Arrange
    my_parameters = {
        "int_parameter" : 100,
        "str_parameter" : "Hello Lyfter team",
        "float_parameter" : 100.80,
        "dictionary_parameter" : {"user_id": 1, "username": "Oscar", "last_name": "Alfaro"},
        "boolean_parameter" : True,
        "none_parameter" : None
    }

    # Act & Assert
    for dic_parameter in my_parameters:
        with pytest.raises(TypeError):
            bubble_sort(dic_parameter)
