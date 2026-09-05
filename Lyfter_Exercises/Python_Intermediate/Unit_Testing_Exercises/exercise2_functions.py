def sum_numbers_in_list(my_list):
    if my_list == []:
        raise ValueError("The is empty")
    total_sum = 0
    for num in my_list:
        if not isinstance(num, (float, int)):
            raise TypeError(f"The element '{num}' in the list is not numeric.")
        total_sum += num
    return total_sum

def reverse_string(my_string):
    if not isinstance(my_string, str):
        raise TypeError(f"The parameter '{my_string} is not a string'")
    if len(my_string) > 80:
        raise ValueError(f"The character limit is 80, you entered {len(my_string)}")
    reversed_string = ""
    for index, letter in enumerate(my_string):
        reversed_string += my_string[len(my_string) - (index + 1)]
    return reversed_string

def print_upper_and_lower_num_in_string(my_string):
    if my_string is None:
        raise ValueError("The string cannot be None")
    if not my_string.strip():
        raise ValueError("The string cannot be empty")
    
    num_upper_letters = 0
    num_lower_letters = 0
    for letter in my_string:
        if letter.isdigit():
            raise TypeError("The string contains numbers.")
        if letter.isupper() and letter != " ":
            num_upper_letters += 1
        elif letter.islower():
            num_lower_letters += 1
    print(f"He have {num_upper_letters} upper cases and {num_lower_letters} cases.")

def order_words_in_a_string(my_string_with_middle_dash):
    my_list = []
    word = ""
    num_of_words = 0
    for letter in my_string_with_middle_dash:
        if letter == " ":
            raise ValueError("The string cannot contains spaces")
        if letter != "-":
            word += letter
        else:
            my_list.append(word)
            num_of_words += 1
            word = ""
    my_list.append(word)
    num_of_words += 1
    if num_of_words > 6:
        raise ValueError("The list cannot contain more that 6 words")
    print(f"Num words: {num_of_words}")
    string_to_return = ""
    for index, word_in_list in enumerate(sorted(my_list)):
        if my_list[index] != my_list[len(my_list) - 1]:
                    string_to_return += word_in_list + "-"
        else:
            string_to_return += word_in_list

    return string_to_return

def return_prime_numbers(list_of_numbers):
    if list_of_numbers == None:
        raise TypeError("The list cannot be None")
    if list_of_numbers == []:
        raise ValueError("The list cannot be empty")
    list_to_return = []
    for num_in_list in list_of_numbers:
        if num_in_list <= 1:
            continue
        is_prime = True
        for i in range(2, num_in_list):
            if num_in_list % i == 0:
                is_prime = False
                break
        if is_prime:
            list_to_return.append(num_in_list)
    return list_to_return

