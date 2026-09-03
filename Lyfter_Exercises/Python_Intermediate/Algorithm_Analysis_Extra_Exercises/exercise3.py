def print_all_pairs(my_dict):
    for key1 in my_dict:  # O(n)
        for key2 in my_dict:  # O(n^2)
            print(f"{key1}-{key2}")  # O(1)


##--------- EXPLANATION ##---------
# O(n^2), where n is the number of keys in the dictionary. Both loops iterate over the
# same dictionary, so the inner print runs n * n times in total.
# Space complexity is O(1): it does not store anything, it only prints.
# It takes 1_000_000^2 = 1_000_000_000_000 iterations

