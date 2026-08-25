print("----- Calculate Average of greater value -----")

my_list = [10, 20, 30, 40, 50]

sum_of_numbers = 0
for number in my_list:
    sum_of_numbers += number
average = sum_of_numbers / len(my_list)
new_list = []

for number in my_list:
    if number > average:
        new_list.append(number)

print("The average of the list is:", average)
print("The numbers greater than the average are:", new_list)


#Planning:
#Sum all numbers and divide by the length of the list to get the average
#Create a new list containing only the numbers greater than the average