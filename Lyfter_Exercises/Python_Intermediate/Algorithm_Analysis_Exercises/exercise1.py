def bubble_sort(unordered_list):
    for global_index in range(0, len(unordered_list) - 1): # O(n)
        changes_made = False # O(1)
        for index_list in range(0, len(unordered_list) - 1 - global_index): # O(n^2)
            current_element = unordered_list[index_list] # O(1)
            next_element = unordered_list[index_list + 1] # O(1)

            if current_element > next_element: # O(1)
                unordered_list[index_list] = next_element # O(1)
                unordered_list[index_list + 1] = current_element # O(1)
                changes_made = True # O(1)
                print(unordered_list) # O(1)
        if not changes_made: # O(1)
            return # O(1)


my_unordered_list = [10, 60, 40, 70, 30, 50, 0, 20] # O(1)
bubble_sort(my_unordered_list) # O(n^2)
print("<----------------------------->") # O(1)
print(f"FINAL ORDERED LIST: {my_unordered_list}") # O(1)