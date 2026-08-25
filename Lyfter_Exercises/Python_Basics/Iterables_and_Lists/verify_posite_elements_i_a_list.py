print("----- Verify Positive Elements in a List -----")

my_list = [3, 6, 10, -2, 4]

negative_counter = 0
for number in my_list:
    if number <= 0:
        negative_counter += 1
if negative_counter == 0:
    print(f"All elements in the list are positive numbers")
else:
    print(f"There is at least one negative number in the list or zero")