def bubble_sort(my_list):
    if not isinstance(my_list, list):
        raise TypeError(f"Expected a list, got {type(my_list).__name__}")
    
    for global_index in range(0, len(my_list) - 1):
        changes_made = False
        for internal_index in range(0, len(my_list) - 1 - global_index):
            current_element = my_list[internal_index]
            next_element = my_list[internal_index + 1]

            if current_element > next_element:
                my_list[internal_index] = next_element
                my_list[internal_index + 1] = current_element
                changes_made = True
        if not changes_made:
            return my_list
    return my_list

unordered_list = []
try:
    ordered_list = bubble_sort(unordered_list)
    print(ordered_list)
except TypeError as e:
    print(e)