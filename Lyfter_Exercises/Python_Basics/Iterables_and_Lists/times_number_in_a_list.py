print("----- Times Number in a List -----")

my_list = input("Enter a list of numbers separated by spaces: ").split()

num_to_search = input("Enter a number to search for: ")

counter = 0
for number in my_list:
    if int(number) == int(num_to_search):
        counter += 1
print(f"The number {num_to_search} appears {counter} times in the list.")
      
