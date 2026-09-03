def bubble_sort(unordered_list):
    for global_index in range(0, len(unordered_list) - 1):
        changes_made = False
        for index_list in range(0, len(unordered_list) - 1 - global_index):
            last_element_index = len(unordered_list) - (index_list + 1)
            last_element = unordered_list[last_element_index]
            prev_element_index = len(unordered_list) - (index_list + 2)
            prev_element = unordered_list[prev_element_index]

            if last_element < prev_element:
                unordered_list[last_element_index] = prev_element
                unordered_list[prev_element_index] = last_element
                changes_made = True
                print(unordered_list)
        if not changes_made:
            return


my_unordered_list = [10, 60, 40, 70, 30, 50, 0, 20]
bubble_sort(my_unordered_list)
print("<----------------------------->")
print(f"FINAL ORDERED LIST: {my_unordered_list}")