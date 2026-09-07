def bubble_sort(unordered_list):
    for global_index in range(0, len(unordered_list) - 1):
        changes_made = False
        for index_list in range(0, len(unordered_list) - 1 - global_index):
            current_element = unordered_list[index_list]
            next_element = unordered_list[index_list + 1]

            if current_element > next_element:
                unordered_list[index_list] = next_element
                unordered_list[index_list + 1] = current_element
                changes_made = True
                print(unordered_list)
        if not changes_made:
            return


my_unordered_list = [10, 60, 40, 70, 30, 50, 0, 20]
bubble_sort(my_unordered_list)
print("<----------------------------->")
print(f"FINAL ORDERED LIST: {my_unordered_list}")