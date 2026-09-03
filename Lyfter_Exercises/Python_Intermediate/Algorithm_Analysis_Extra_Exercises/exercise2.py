import time

def linear_search(my_list, target):
    for item in my_list:  # O(n)
        if item == target:  # O(1)
            return True  # O(1)
    return False  # O(1)

def binary_search(my_list, target):
    low = 0  # O(1)
    high = len(my_list) - 1  # O(1)
    while low <= high:  # O(log n)
        mid = (low + high) // 2  # O(1)
        if my_list[mid] == target:  # O(1)
            return True  # O(1)
        elif my_list[mid] < target:  # O(1)
            low = mid + 1  # O(1)
        else:  
            high = mid - 1  # O(1)
    return False  # O(1)


##--------- EXPLANATION ##---------
# 1. What is the complexity of each algorithm?
# linear_search: O(n) in the worst case (target is last or not present), O(1) in the
#   best case (target is first). Space: O(1).
# binary_search: O(log n) in the worst case, because it discards half of the remaining
#   elements on every iteration. O(1) in the best case (target lands on the first mid).
#   Space: O(1).

# 2. When should each one be used?
# linear_search: when the list is unsorted, when it is small, or when we only search
#   once (sorting costs O(n log n), which is more expensive than a single linear scan).
#   Also for structures without index access, like a linked list.
# binary_search: when the list is already sorted, the list is large, and we search many
#   times, so the cost of sorting is paid once and amortized across all the searches.

# 3. What happens if the list is not sorted?
# binary_search returns wrong results. It does not raise an error and it does not crash,
# it just silently returns False for elements that are actually in the list. The
# algorithm assumes that everything to the right of mid is greater, so when that
# assumption is false it discards the half where the target was. A sorted list is a
# precondition, not an optimization.

my_own_list = list(range(10_000_000)) # Ordered list from 0 to 9999999
target = 9_999_999  # The worst case for linear_search

start_linear = time.perf_counter()
result_linear_search = linear_search(my_own_list, target)
end_linear = time.perf_counter()
print(f"LINEAR RESULT: {result_linear_search}, it took: {end_linear - start_linear}")

start_binary = time.perf_counter()
result_binary_search = binary_search(my_own_list, target)
end_binary = time.perf_counter()
print(f"BINARY RESULT: {result_binary_search}, it took: {end_binary - start_binary}")



