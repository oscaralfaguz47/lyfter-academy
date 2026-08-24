print("----- Times a character is in a text -----")

def get_num_of_chars_in_text (text, char):
    counter = 0
    for letter in text:
        if letter == char:
            counter += 1
    return counter

text = input("Enter a word: ")
char_to_count = input("Enter the character you want to count: ")

num_times = get_num_of_chars_in_text(text, char_to_count)
print(f'El character "{char_to_count}" is presented {num_times} times in the word "{text}"')