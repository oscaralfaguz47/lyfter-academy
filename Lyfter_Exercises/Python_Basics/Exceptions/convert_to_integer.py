print("----- Convert a list of string to integers -----")


def convert_to_integer(my_list_of_strings):
    print("Results:")
    for element in my_list_of_strings:
        try:
            int(element)
            print(f'"{element}" converted to {element}')
        except ValueError:
            print(f"The element '{element}' couldn't be converted")

my_list = ['4', 'hola', '10', '5.2']
convert_to_integer(my_list)
















# Function that:
# - Receives a list of strings
# - Try convert every element to int
# - Use try to catch all the errors
# - If I cannot convert, then print= "The element cannot be converted"
# - If success the Print: "4" converted to 4