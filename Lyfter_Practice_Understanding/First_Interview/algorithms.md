# Algorithms in 2 Cards

The 2 topics: **Bubble Sort** and **Big O**.

Read Big O first if you want, but Bubble Sort is the example that makes Big O click.

---

# 1. Bubble Sort

> **Bubble sort** compares two items next to each other and swaps them if they are in the wrong order. On every pass, the biggest item left "bubbles up" to the end.

## How it works, step by step

```
Start:  [5, 1, 4, 2]

PASS 1
[5, 1, 4, 2]   5 > 1 ?  yes -> swap
[1, 5, 4, 2]   5 > 4 ?  yes -> swap
[1, 4, 5, 2]   5 > 2 ?  yes -> swap
[1, 4, 2, 5]   <- 5 is now in its final place

PASS 2
[1, 4, 2, 5]   1 > 4 ?  no
[1, 4, 2, 5]   4 > 2 ?  yes -> swap
[1, 2, 4, 5]   <- 4 is now in its final place

PASS 3
[1, 2, 4, 5]   1 > 2 ?  no  -> no swaps at all -> STOP, it's sorted
```

The end of the list gets sorted first. That's why each pass can be shorter than the one before.

## The code

```python
def bubble_sort(items):
    n = len(items)
    for i in range(n - 1):                  # n-1 passes
        swapped = False
        for j in range(n - 1 - i):          # "- i": the end is already sorted
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]    # swap
                swapped = True
        if not swapped:                     # nothing moved -> it's sorted
            break
    return items

print(bubble_sort([64, 34, 25, 12, 22, 11, 90]))
# [11, 12, 22, 25, 34, 90]
```

## The 4 details that show you understand it

| Detail | Why it matters |
|---|---|
| `n - 1 - i` | The end of the list is already sorted. Without `- i` it still works, but you compare sorted items again for nothing. |
| `swapped` flag | If one full pass makes no swaps, the list is already sorted. This turns the best case into O(n). |
| `a, b = b, a` | Python swaps in one line. No temporary variable needed. |
| `>` and not `>=` | With `>` it is **stable**: equal items keep their original order. |

## Speed

| Case | Big O | When |
|---|---|---|
| **Best** | **O(n)** | Already sorted. One pass, no swaps, the flag stops it. |
| **Average** | **O(n²)** | Random order. |
| **Worst** | **O(n²)** | Backwards order. |
| **Space** | **O(1)** | It sorts in place. No extra list needed. |

**Why O(n²):** two loops inside each other, each over about n items.
The exact number of comparisons is `(n-1) + (n-2) + ... + 1 = n(n-1)/2`, which is O(n²).

Three words to describe it: **stable**, **in place**, **adaptive** (with the flag).

## Trap: it changes the list, so watch the return

```python
numbers = [3, 1, 2]

numbers = numbers.sort()      # BAD: numbers is now None
numbers.sort()                # OK: changes the list, returns None
sorted_copy = sorted(numbers) # OK: returns a NEW list
```

Same for your own function: if `bubble_sort` changes the list **and** has `return items`, both ways work. If you forget the `return`, then `result = bubble_sort(x)` gives you `None`.

If you don't want to touch the caller's list:

```python
def bubble_sort(items):
    items = items.copy()      # work on a copy
    ...
    return items
```

## Why nobody uses it in real code

With 10,000 items:

| Algorithm | Comparisons |
|---|---|
| Bubble sort — O(n²) | ~50,000,000 |
| A good sort — O(n log n) | ~130,000 |

About **380 times** fewer.

Python's `sorted()` and `.sort()` use **Timsort**: O(n log n), stable, and extra fast on lists that are already partly sorted. Always use that in real code.

**So why do interviews ask for it?** Because it is the simplest way to check if you can reason about nested loops, index limits, in-place changes, and Big O. It's a thinking test, not a practical one.

If they ask when you would use it, the honest answer is: *"Almost never. Only for very small or nearly sorted lists, or for teaching. In real code I use `sorted()`, which is Timsort."*

## Sorting algorithms compared

| Algorithm | Average | Worst | Space | Stable |
|---|---|---|---|---|
| Bubble | O(n²) | O(n²) | O(1) | yes |
| Selection | O(n²) | O(n²) | O(1) | no |
| Insertion | O(n²) | O(n²) | O(1) | yes |
| Merge | O(n log n) | O(n log n) | O(n) | yes |
| Quick | O(n log n) | O(n²) | O(log n) | no |
| **Timsort** (Python) | O(n log n) | O(n log n) | O(n) | yes |

---

# 2. Big O

> **Big O** describes how much **slower** or **bigger** something gets as the input grows.
> It is not about seconds. It is about **how well it scales**.

## The idea

You drop the constants and the small parts, because with a big `n` only the biggest part matters:

```
O(3n² + 5n + 100)  ->  O(n²)
```

Why: with n = 1,000,000 the `n²` part is enormous and everything else is noise. Constants also depend on the computer, which is not what you're measuring.

## The list to memorize

| Notation | Name | Example |
|---|---|---|
| **O(1)** | Constant | `my_list[0]`, `my_dict[key]`, `stack.push()` |
| **O(log n)** | Logarithmic | Binary search, lookup in a balanced tree |
| **O(n)** | Linear | Going through a list, `in` on a list |
| **O(n log n)** | Linearithmic | `sorted()`, merge sort, quicksort |
| **O(n²)** | Quadratic | Bubble sort, two loops inside each other |
| **O(2ⁿ)** | Exponential | Recursive Fibonacci with no cache |
| **O(n!)** | Factorial | Trying every possible order |

## Why it matters — n = 1,000,000

| | Operations |
|---|---|
| O(log n) | ~20 |
| O(n) | 1,000,000 |
| O(n log n) | ~20,000,000 |
| O(n²) | 1,000,000,000,000 |

That gap is the whole point. The constant doesn't matter. The **shape of the growth** is everything.

## How to read code

```python
def example(items):              # n = len(items)
    total = 0                    # O(1)

    for x in items:              # O(n)
        total += x               #   O(1) inside

    for x in items:              # O(n)
        for y in items:          #   O(n) -> runs n times per outer round
            print(x, y)          #   => O(n²)

    return total                 # O(1)

# O(1) + O(n) + O(n²) + O(1)  =  O(n²)   <- the biggest one wins
```

## The 3 rules

```
1. Loops one after another  ->  ADD       O(n) + O(n) = O(n)
2. Loops inside each other  ->  MULTIPLY  O(n) x O(n) = O(n²)
3. Cutting the problem in half each step  ->  O(log n)
```

**Why half means log n:** how many times can you divide 1,000,000 by 2 until you reach 1?
About 20. That is log₂(1,000,000).

## Time and space are two different things

| Algorithm | Time | Space |
|---|---|---|
| Bubble sort | O(n²) | O(1) — sorts in place |
| Merge sort | O(n log n) | O(n) — needs extra lists |

The classic trade: you buy speed with memory.

```python
# O(2ⁿ) -> it recalculates the same values over and over
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# O(n) time, O(n) space -> it remembers the results
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

## The Python table you should know by heart

| Operation | `list` | `dict` / `set` |
|---|---|---|
| Get by index or key | O(1) | O(1) |
| Search with `in` | **O(n)** | **O(1)** |
| Add at the end | O(1)* | O(1) |
| Add at the start | **O(n)** | — |
| Delete | O(n) | O(1) |
| `sorted()` | O(n log n) | — |

\* "amortized" O(1): once in a while the list needs more room and copies everything (O(n)), but since it doubles its size, that cost spreads out and averages to O(1).

## The most useful Big O trick in daily Python

`x in my_list` is **O(n)**. `x in my_set` is **O(1)**.

```python
# O(n x m)  -> slow
for item in items:
    if item in big_list:
        ...

# O(n + m)  -> fast
lookup = set(big_list)            # build the set once
for item in items:
    if item in lookup:
        ...
```

Turning a list into a set before repeated searches changes a quadratic loop into a linear one. This is the one you will actually use at work.

## The relatives of Big O

| Symbol | Bound | Meaning |
|---|---|---|
| **O** (Big O) | Upper | Worst case |
| **Ω** (Omega) | Lower | Best case |
| **Θ** (Theta) | Both | They are the same |

In interviews people say "Big O" but usually mean the average or worst case. Only bring this up if they push.

---

# Cheat sheet

```
BUBBLE SORT  -> compare neighbours, swap, biggest floats to the end
                O(n²) normal, O(n) best case with the swapped flag
                O(1) space, stable, in place
                Real code: use sorted() -> Timsort, O(n log n)

BIG O        -> how it scales, not how fast it is
                Drop constants, keep the biggest part
                Loops side by side  -> add
                Loops inside loops  -> multiply
                Cutting in half     -> log n
                "in" on a list O(n), on a set O(1)  <- use this one
```

---

# Quick self-test

Cover the right column. Answer out loud.

| Question | Answer |
|---|---|
| How does bubble sort work? | It compares items next to each other and swaps them if they are in the wrong order, so the biggest one moves to the end on each pass. |
| Why is it O(n²)? | Two loops inside each other, each over about n items. |
| What is its best case and why? | O(n), if you add a flag that stops the loop when a full pass makes no swaps. |
| How much space does it use? | O(1). It sorts in place, no extra list. |
| Is it stable? | Yes, as long as you compare with `>` and not `>=`. |
| Why `n - 1 - i` in the inner loop? | Because the end of the list is already sorted after each pass. |
| What does Python use to sort? | Timsort — O(n log n), stable, fast on partly sorted data. |
| Would you use bubble sort at work? | No. Only for very small lists or for teaching. |
| What is Big O? | A description of how the time or space grows as the input grows. |
| Why drop the constants? | Because with a big input only the biggest part matters, and constants depend on the machine. |
| Loops one after another? | Add them: O(n) + O(n) = O(n). |
| Loops inside each other? | Multiply them: O(n) x O(n) = O(n²). |
| When do you get O(log n)? | When each step cuts the problem in half. |
| What is the cost of `in` on a list? | O(n). On a set or dict it is O(1). |
| How do you make repeated searches faster? | Turn the list into a set first. That turns O(n x m) into O(n + m). |
| What does "amortized O(1)" mean? | Once in a while an operation costs O(n), but spread over many calls it averages to O(1). |
| Time and space — same thing? | No, two separate measures. Bubble sort is O(n²) time but O(1) space. |
| Give an O(2ⁿ) example. | Recursive Fibonacci with no cache. With `lru_cache` it drops to O(n). |