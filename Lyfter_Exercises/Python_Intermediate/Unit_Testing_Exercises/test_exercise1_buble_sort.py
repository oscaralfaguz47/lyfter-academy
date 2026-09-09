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

@pytest.mark.parametrize("invalid_parameter", [
    100,
    "Hello Lyfter team",
    100.80,
    {"user_id":1, "username": "Oscar", "last_name": "Alfaro"},
    True,
    None
])
def test_bubble_sort_raises_type_error_with_non_list_parameter(invalid_parameter):
    # Act & Assert
    with pytest.raises(TypeError, match="Expected a list"):
        bubble_sort(invalid_parameter)
