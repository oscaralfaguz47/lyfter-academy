print("----- One Dictionary from Two Lists -----")

list_a = ['name', 'age', 'marital_status', 'salary', 'country']
list_b = ['Carlos Francisco', 35, 'single', 5000, 'Argentina']

my_dictionary = {}

for index_list_a, value_list_a in enumerate(list_a):
    my_dictionary[value_list_a] = list_b[index_list_a]
print("My dictionary: ", my_dictionary)


