# Python in 7 Cards

The 7 topics: **data types, iterations, exceptions, scope, file handling, infinite parameters, decorators.**

Each card has: the short definition, the code, and the trap to avoid.

---

# 1. Data Types

> A **data type** tells Python what kind of value something is and what you can do with it.

## The full list

```python
# Numbers
age     = 30              # int
price   = 19.99           # float
z       = 3 + 4j          # complex
active  = True            # bool

# Text
name    = "Oscar"         # str

# Sequences
items   = [1, 2, 3]       # list      -> ordered, changeable
point   = (10, 20)        # tuple     -> ordered, fixed
numbers = range(5)        # range     -> 0,1,2,3,4

# Mapping
user    = {"name": "Oscar", "age": 30}    # dict -> key/value

# Sets
unique  = {1, 2, 3}       # set       -> no duplicates, changeable
frozen  = frozenset([1, 2])               # frozenset -> no duplicates, fixed

# Binary
data    = b"hello"        # bytes
buffer  = bytearray(b"hello")             # bytearray

# Nothing
empty   = None            # NoneType
```

## The one thing that really matters: mutable vs immutable

> **Mutable** = you can change it after you create it.
> **Immutable** = you cannot. Any "change" makes a brand new object.

```python
# MUTABLE -> same object, changed in place
items = [1, 2, 3]
print(id(items))          # 140234...
items.append(4)
print(id(items))          # 140234...  <- SAME id, same object

# IMMUTABLE -> a new object is created
text = "hello"
print(id(text))           # 140567...
text += " world"
print(id(text))           # 140999...  <- DIFFERENT id, new object
```

| Mutable | Immutable |
|---|---|
| `list`, `dict`, `set`, `bytearray` | `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`, `None` |

## Why it matters

```python
# 1. Mutable objects are SHARED, not copied
a = [1, 2, 3]
b = a                     # b is not a copy, it's the same list
b.append(4)
print(a)                  # [1, 2, 3, 4]  <- both changed!

c = a.copy()              # this is a real copy
c.append(5)
print(a)                  # [1, 2, 3, 4]  <- safe

# 2. Only immutable things can be dict keys
{(1, 2): "ok"}            # tuple works
{[1, 2]: "no"}            # TypeError: unhashable type: 'list'
```

## Python's typing

```python
x = 5                     # DYNAMIC: the type is decided while running
x = "hello"               # you can change it, no declaration needed

"1" + 1                   # TypeError -> STRONG: no silent conversions
"1" + str(1)              # "11"      -> you must convert on purpose
```

## Traps

```python
# TRAP 1: forgetting to save the converted value
number = "3.5"
float(number)             # does nothing, the result is thrown away
number = float(number)    # correct

# TRAP 2: a mutable default argument
def add(item, items=[]):  # BAD: the list is created ONCE and reused
    items.append(item)
    return items

print(add("a"))           # ['a']
print(add("b"))           # ['a', 'b']  <- leaked!

def add(item, items=None):    # GOOD
    if items is None:
        items = []
    items.append(item)
    return items

# TRAP 3: floats are not exact
0.1 + 0.2 == 0.3          # False
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")     # True -> use this for money
```

---

# 2. Iterations

> An **iteration** is going through the items of a collection one at a time, running the same block of code for each one.

## The two loops

```python
# FOR -> when you know what you are going through
for fruit in ["apple", "banana", "grape"]:
    print(fruit)

# WHILE -> when you loop until something changes
count = 0
while count < 3:
    print(count)
    count += 1            # careful: += , not =+
```

## Control: break, continue, else

```python
for number in range(10):
    if number == 7:
        print("found")
        break             # leave the loop completely
    if number % 2 == 0:
        continue          # skip to the next round
    print(number)
else:
    print("not found")    # runs ONLY if the loop ended with no break
```

`for...else` is rarely known. The `else` means "the loop finished without breaking".

## The helpers you should use

```python
fruits = ["apple", "banana", "grape"]
prices = [100, 250, 80]

for i, fruit in enumerate(fruits, start=1):     # index + value
    print(f"{i}. {fruit}")

for fruit, price in zip(fruits, prices):        # two lists at once
    print(f"{fruit}: {price}")

for fruit in reversed(fruits): ...
for fruit in sorted(fruits): ...
```

Don't write `for i in range(len(my_list))` just to get the index. Use `enumerate`.

## Going through a dictionary

```python
user = {"name": "Oscar", "age": 30}

for key in user:                  # KEYS <- this is the default!
    print(key)

for value in user.values():       # values
    print(value)

for key, value in user.items():   # both
    print(f"{key}: {value}")
```

## How a for loop really works

```python
# for x in my_list:  is really this:
it = iter(my_list)                # get an iterator
while True:
    try:
        x = next(it)              # ask for the next item
        # loop body
    except StopIteration:         # no more items
        break
```

That's why anything with `__iter__` can be looped: lists, strings, dicts, files, generators.

## Iterable vs iterator vs generator

```python
# ITERABLE -> something you can loop over
my_list = [1, 2, 3]

# ITERATOR -> gives one value at a time and remembers where it is
it = iter(my_list)
print(next(it))       # 1
print(next(it))       # 2

# GENERATOR -> an iterator built with yield. Lazy: makes values one by one.
def count_to(n):
    i = 1
    while i <= n:
        yield i       # pauses here, continues on the next call
        i += 1

for number in count_to(3):
    print(number)
```

A list of a million items sits in memory. A generator makes one at a time. That's why you can loop over a 10 GB file.

## Comprehensions

```python
squares = [n ** 2 for n in range(5)]              # [0, 1, 4, 9, 16]
evens   = [n for n in range(10) if n % 2 == 0]    # with a filter
mapping = {n: n ** 2 for n in range(4)}           # dict
unique  = {letter for letter in "banana"}         # set
lazy    = (n ** 2 for n in range(1000000))        # generator, no memory used
```

## Trap: never change a list while looping over it

```python
numbers = [1, 2, 3, 4, 5, 6]

for n in numbers:                 # BAD: it skips items
    if n % 2 == 0:
        numbers.remove(n)

for n in numbers.copy():          # OK: loop over a copy
    if n % 2 == 0:
        numbers.remove(n)

numbers = [n for n in numbers if n % 2 != 0]      # BEST: build a new list
```

## Trap: changing the loop variable does nothing

```python
numbers = [1, 2, 3]

for n in numbers:
    n = n * 2                     # only changes the local name
print(numbers)                    # [1, 2, 3]  <- untouched

for i in range(len(numbers)):
    numbers[i] *= 2               # this really changes the list
print(numbers)                    # [2, 4, 6]
```

---

# 3. Exceptions

> An **exception** is an error that happens while the program runs and stops the normal flow. If nobody catches it, the program crashes.

## The full structure

```python
try:
    number = int(input("Number: "))
    result = 10 / number
except ValueError:
    print("That is not a number")
except ZeroDivisionError as error:
    print(f"Cannot divide by zero: {error}")
except (TypeError, KeyError):
    print("Type or key error")
else:
    print(f"Result: {result}")    # runs ONLY if there was no error
finally:
    print("Always runs")          # runs ALWAYS, error or not
```

| Block | When it runs |
|---|---|
| `try` | The risky code |
| `except` | Only if that error happened |
| `else` | Only if there was NO error |
| `finally` | Always, no matter what |

## The family tree

```
BaseException
 +-- Exception
      +-- ArithmeticError  -> ZeroDivisionError
      +-- LookupError      -> IndexError, KeyError
      +-- ValueError
      +-- TypeError
      +-- OSError          -> FileNotFoundError, PermissionError
      +-- AttributeError, NameError, ...
```

**Rule:** catch from **specific to general**. Never use a bare `except:` — it even catches `Ctrl+C`.

## Raising your own

```python
class NotEnoughMoneyError(Exception):       # your own exception type
    """Raised when the account does not have enough funds."""
    pass

class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise NotEnoughMoneyError(f"Balance: {self.balance}, asked: {amount}")
        self.balance -= amount
        return self.balance

account = Account(1000)
try:
    account.withdraw(5000)
except NotEnoughMoneyError as error:
    print(error)
```

## Trap: everything that depends on the risky line goes INSIDE the try

```python
# BAD
try:
    age = int(input("Age: "))
except ValueError:
    print("Invalid")
print(age)                # NameError if it went to the except!

# GOOD
try:
    age = int(input("Age: "))
    print(age)
except ValueError:
    print("Invalid")
```

## Checking values: `isdigit()` vs `try/except`

```python
"-5".isdigit()            # False  <- does not work for negatives
"3.5".isdigit()           # False  <- does not work for decimals

def to_int(text):         # the Python way
    try:
        return int(text)
    except ValueError:
        return None
```

Python prefers **"try it and catch the error"** over **"check everything first"**.

---

# 4. Scope

> **Scope** is the part of the code where a variable can be seen and used.

## The LEGB rule

Python looks for a name in this order and stops at the first match:

```
L -> Local      (inside the current function)
E -> Enclosing  (the outer function, if nested)
G -> Global     (top of the file)
B -> Built-in   (print, len, sum...)
```

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)          # local

    inner()
    print(x)              # enclosing

outer()
print(x)                  # global
```

## Reading vs writing

A function can **read** an outer variable. But if you **assign** to it, Python makes a new local one instead.

```python
count = 0

def increase():
    count += 1            # UnboundLocalError! Python thinks count is local

def increase():
    global count          # now it changes the one at the top of the file
    count += 1

def make_counter():
    total = 0
    def add(n):
        nonlocal total    # changes the one in the outer FUNCTION
        total += n
        return total
    return add

add = make_counter()
print(add(5))             # 5
print(add(3))             # 8   <- it remembers
```

| Keyword | Changes the variable in |
|---|---|
| `global` | The top of the file |
| `nonlocal` | The outer function |

## Trap: don't use built-in names

```python
sum = 0                   # you just broke the built-in sum() here
for n in [1, 2, 3]:
    sum += n
print(sum([1, 2]))        # TypeError: 'int' object is not callable

total = 0                 # use this instead
```

Names people break by accident: `sum`, `list`, `dict`, `str`, `type`, `id`, `input`, `max`, `min`, `filter`.

---

# 5. File Handling

> **File handling** is reading and writing files on disk, so your data still exists after the program ends.

## The modes

| Mode | What it does |
|---|---|
| `"r"` | Read. Error if the file is not there |
| `"w"` | Write. **Erases** everything first |
| `"a"` | Append. Writes at the end |
| `"x"` | Create. Error if it already exists |
| `"r+"` | Read and write |
| `"rb"` / `"wb"` | Binary (images, PDFs) |

## Always use `with`

```python
# READING
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()         # the whole file as one string
    # file.readlines()            # a list of lines
    # for line in file: ...       # one line at a time, uses little memory

# WRITING
with open("data.txt", "a", encoding="utf-8") as file:
    file.write("new line\n")
```

`with` is a **context manager**. It closes the file for you, even if an error happens in the middle. Without it you would need `try/finally` and `file.close()`.

## Paths that always work

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent      # the folder of THIS file
FILE_PATH = BASE_DIR / "data" / "records.csv"

FILE_PATH.parent.mkdir(parents=True, exist_ok=True)     # create the folder
print(FILE_PATH.exists())
```

This way the path does not depend on the folder you run the script from.

## CSV

```python
import csv

FIELDS = ["id", "amount", "category"]

def save(row: dict) -> None:
    write_header = not FILE_PATH.exists()
    with open(FILE_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

def load() -> list[dict]:
    if not FILE_PATH.exists():
        return []                 # return [], never None
    with open(FILE_PATH, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))
```

Two small things that save you: `newline=""` stops empty rows on Windows, and returning `[]` instead of `None` stops `AttributeError: 'NoneType' object has no attribute...` later on.

---

# 6. Infinite Parameters

> **Infinite parameters** let a function take any number of arguments, when you don't know how many will come.

## The two of them

```python
def show(*args, **kwargs):
    print(args)       # a TUPLE of positional arguments
    print(kwargs)     # a DICT of named arguments

show(1, 2, 3, name="Oscar", age=30)
# (1, 2, 3)
# {'name': 'Oscar', 'age': 30}
```

| | Collects | Into a |
|---|---|---|
| `*args` | Extra **positional** arguments | tuple |
| `**kwargs` | Extra **named** arguments | dict |

The names don't matter (`*numbers`, `**options` work the same). What matters is the `*` and the `**`.

## A real example

```python
def add(*numbers):
    total = 0
    for number in numbers:
        total += number
    return total

print(add(1, 2, 3, 4))    # 10
print(add())              # 0   <- empty case works too
```

## The order you must follow

```python
def example(normal, with_default=10, *args, named_only, **kwargs):
    ...
```

```
normal  ->  with default  ->  *args  ->  named only  ->  **kwargs
```

## Unpacking: the same symbols, the other way around

In a **definition** they **collect**. In a **call** they **spread out**.

```python
values = [1, 2, 3]
config = {"name": "Oscar", "age": 30}

add(*values)              # same as add(1, 2, 3)

def create_user(name, age):
    return f"{name} ({age})"

create_user(**config)     # same as create_user(name="Oscar", age=30)
```

This is exactly why decorators are written as `def wrapper(*args, **kwargs): return func(*args, **kwargs)` — they take whatever comes in and pass it straight through, so the decorator works on any function.

---

# 7. Decorators

> A **decorator** is a function that takes another function, adds something to it, and gives back the new version — without touching the original code.

## Why it works: functions are objects

```python
def greet(name):
    return f"Hello {name}"

f = greet                 # you can assign it (no parentheses!)
print(f("Oscar"))         # Hello Oscar
print(greet.__name__)     # 'greet'  <- it's an object with attributes
```

You can assign functions, pass them as arguments, and return them. That's the whole trick.

## Building one

```python
import functools

def log(func):                        # 1. takes the function
    @functools.wraps(func)
    def wrapper(*args, **kwargs):     # 2. takes whatever arguments
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} finished")
        return result                 # <- RETURN #1
    return wrapper                    # <- RETURN #2

@log
def add(a, b):
    return a + b

print(add(2, 3))
```

## `@` is just a shortcut

```python
@log
def add(a, b):
    return a + b

# is exactly the same as:

def add(a, b):
    return a + b
add = log(add)
```

The `@` runs when Python **reads** the `def`, not when you call the function.

## The two returns that break everything

```python
# BUG 1: no return inside wrapper
def broken(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)         # runs it but throws the result away
    return wrapper
# add(2, 3) -> None

# BUG 2: no return of wrapper
def broken(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    # missing: return wrapper
# broken returns None -> add becomes None -> TypeError
```

## Why `functools.wraps`

```python
@log
def add(a, b):
    """Adds two numbers."""
    return a + b

print(add.__name__)       # 'add'   <- with @wraps
                          # 'wrapper' <- without it
```

It copies the original name and docstring. Important for debugging and for any tool that reads function info.

## Decorators with arguments: 3 levels

```python
import functools

def repeat(times):                         # 1. takes the ARGUMENT
    def decorator(func):                   # 2. takes the FUNCTION
        @functools.wraps(func)
        def wrapper(*args, **kwargs):      # 3. takes the CALL's arguments
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello {name}")
```

**Why 3 levels:** `@repeat(times=3)` **calls** `repeat` first, and whatever comes back is the real decorator.

```python
@log                # no call  -> 2 levels
@repeat(times=3)    # a call   -> 3 levels
```

## Stacking them

```python
@timer
@log
def process():
    ...

# Applied from the bottom up:
# process = timer(log(process))
```

The one closest to the `def` wraps first.

## A useful one

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.4f}s")
        return result
    return wrapper
```

## Built-in decorators to know

| Decorator | What it does |
|---|---|
| `@property` | Makes a method act like a read-only attribute |
| `@x.setter` | Defines how that attribute is written |
| `@staticmethod` | A method with no `self` and no `cls` — just a helper |
| `@classmethod` | Gets `cls` — used for second constructors |
| `@abstractmethod` | Forces the child class to write this method |
| `@functools.wraps` | Keeps the original function's name and docs |
| `@functools.lru_cache` | Remembers results so it doesn't recalculate |

**Used in real life for:** logging, timing, login checks, retries, caching, input validation, and web routes like `@app.route("/")` in Flask.

---

# Cheat sheet

```
DATA TYPES     -> what a value is       | mutable vs immutable is the key
ITERATIONS     -> go through items      | for = known, while = condition
EXCEPTIONS     -> errors while running  | try / except / else / finally
SCOPE          -> where a name is seen  | LEGB: Local, Enclosing, Global, Built-in
FILE HANDLING  -> save data to disk     | always use "with"
*args/**kwargs -> any number of args    | tuple and dict
DECORATORS     -> wrap a function       | needs TWO returns
```

---

# Quick self-test

Cover the right column. Answer out loud.

| Question | Answer |
|---|---|
| Mutable vs immutable? | Mutable can be changed after creation (same object). Immutable cannot — a "change" creates a new object. |
| Name the mutable types. | `list`, `dict`, `set`, `bytearray`. |
| Why can't a list be a dict key? | Keys must be hashable, and only immutable objects are. |
| Is Python typed? | Dynamically (type decided while running) and strongly (no silent conversions). |
| What is an iteration? | Going through the items of a collection one at a time. |
| How does a `for` really work? | It calls `iter()` to get an iterator, then `next()` until `StopIteration`. |
| Iterable vs iterator? | An iterable is something you can loop over. An iterator gives one value at a time and remembers its position. |
| What is a generator? | An iterator built with `yield`. It makes values one by one instead of storing them all. |
| What does `for x in my_dict` give you? | The **keys**. Use `.values()` or `.items()` for the rest. |
| What is an exception? | An error that happens while running and stops the normal flow. |
| `else` vs `finally`? | `else` runs only if there was no error. `finally` always runs. |
| How do you make your own exception? | Create a class that inherits from `Exception`, then `raise` it. |
| What is scope? | The part of the code where a variable can be seen and used. |
| What is LEGB? | The search order: Local, Enclosing, Global, Built-in. |
| `global` vs `nonlocal`? | `global` changes the file-level variable. `nonlocal` changes the outer function's one. |
| Why use `with` for files? | It closes the file automatically, even if an error happens. |
| Difference between `"w"` and `"a"`? | `"w"` erases everything first. `"a"` adds at the end. |
| `*args` vs `**kwargs`? | `*args` collects positional arguments into a tuple. `**kwargs` collects named ones into a dict. |
| What does `*` do in a call? | It spreads a list out into separate arguments. |
| What is a decorator? | A function that takes another function, adds behavior, and returns the new version. |
| What is `@decorator` short for? | `my_function = decorator(my_function)`. |
| Why does a decorator need two returns? | One inside `wrapper` to return the result, one to return `wrapper` itself. |
| Why `functools.wraps`? | To keep the original function's name and docstring. |
| Why 3 levels for a decorator with arguments? | Because `@repeat(3)` calls `repeat` first, and what it returns must be the real decorator. |