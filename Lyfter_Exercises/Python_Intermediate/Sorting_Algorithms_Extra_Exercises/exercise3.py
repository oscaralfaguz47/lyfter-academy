def validate_list(list_to_validate):
    if not list_to_validate:
        raise ValueError("The list is empty, you must provide a list with elements")
    
    for index in range(len(list_to_validate)):
        element = list_to_validate[index]
        try:
            list_to_validate[index] = float(element)
        except:
            raise ValueError(f"The element: {element}, is not a valid number")
            

def bubble_sort(list_to_order):
    for global_index in range(0, len(list_to_order) - 1):
        for internal_index in range(0, len(list_to_order) - 1):
            current_element = list_to_order[internal_index]
            next_element = list_to_order[internal_index + 1]

            if current_element > next_element:
                list_to_order[internal_index] = next_element
                list_to_order[internal_index + 1] = current_element

my_list = [50, 70, 10, "78E", -45]

try:
    validate_list(my_list)
    bubble_sort(my_list)
    print(my_list)
except ValueError as e:
    print(e)