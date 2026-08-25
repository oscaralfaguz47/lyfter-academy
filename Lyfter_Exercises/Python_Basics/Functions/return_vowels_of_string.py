print("----- Get the number of vowels of a string -----")

def get_number_of_vowels(my_string):
    num_of_vowels = 0
    my_string_lower = my_string.lower()
    for char in my_string_lower:
        if char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u':
            num_of_vowels += 1
    return num_of_vowels

my_string = input("Enter a word or paragraph: ")
print(f"The string has {get_number_of_vowels(my_string)} vowels.")