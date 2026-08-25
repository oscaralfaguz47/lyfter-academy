print("----- Return a list of words according with the num of letters -----")

def create_list_of_words(list_of_words, number_of_letters):
    new_list = []
    for word in list_of_words:
        if len(word) > number_of_letters:
            new_list.append(word)
    return new_list

list_of_words = input("Write a list of words separated with a space: ").split()
num_of_letters = int(input("Insert the minimum num of letters in the words: "))

print(create_list_of_words(list_of_words, num_of_letters))