print("----- Sum values -----")

def sum_values(my_list_of_strings):
    total_sum = 0
    for element in my_list_of_strings:
        try:
            float(element)
            total_sum += float(element)
            print(f"{float(element)} added correctly")
        except ValueError:
            print(f"Invalid element: {element}")
    print(f"Total sum: {total_sum}")

my_list = ['10', 'manzana', '5.5', '3', 'n/a']
sum_values(my_list)