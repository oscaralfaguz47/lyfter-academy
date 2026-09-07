def manual_add(n):
    result = 0  # O(1)
    for i in range(1, number + 1):  # O(n)
        result += i  # O(1)
    return result  # O(1)

def add_formula(n):
    return number * (number + 1) // 2  # O(1)

##--------- EXPLANATION ##---------
# I would use add_formula because the result is the same and there isn't any iterations that could affect the running time, only one task is executed.
# The manual_add implements a for loop that has to iterate n times to complete the task that at the end the result is going to be the same.

number = 1000000000  # O(1)

result1 = manual_add(number)  # O(n)
print(result1)  # O(1)
result2 = add_formula(number)  # O(1)
print(result2)  # O(1)