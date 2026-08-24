print("----- List with more than four words -----")

word1 = input("Enter the first word: ")
word2 = input("Enter the second word: ")
word3 = input("Enter the third word: ")
word4 = input("Enter the fourth word: ")
word5 = input("Enter the fifth word: ")

my_list = [word1, word2, word3, word4, word5]

long_words = []
for word in my_list:
    if len(word) > 4:
        long_words.append(word)

print("The words with more than four letters are:", long_words)