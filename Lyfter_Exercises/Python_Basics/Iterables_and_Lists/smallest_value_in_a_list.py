print("----- Smallest Value in a List -----")

my_list = [9, 4, -10 ,7, 1, 5, 0, -3]

first_value = my_list[0]
smallest_value = first_value
for number in my_list:
    if number < smallest_value:
        smallest_value = number
print("The smallest value in the list is:", smallest_value)