# OOP in 8 Cards

> **OOP** is a way of writing code where everything is organized into **objects**.
> An object keeps its **data** and its **behavior** together in one place.

One example all the way through: `Animal`.
Each card adds **one new thing** to the card before it.

---

## Part 1: The 4 building blocks

### 1. Class —> *the mold*

> A **class** is a blueprint. It says what data and what behavior its objects will have.

```python
class Animal:                          # <- the CLASS: it defines the shape
    def __init__(self, name):
        self.name = name
```

---

### 2. Object / Instance —> *what comes out of the mold*

> An **object** is a real thing built from a class. Each one has its own data.

```python
buddy = Animal("Buddy")                # <- OBJECT / INSTANCE
max   = Animal("Max")                  # <- another one, with its own data

print(buddy.name)                      # Buddy
print(max.name)                        # Max
```

---

### 3. Attribute —> *what the object HAS*

> An **attribute** is a variable that holds the object's data.

```python
class Animal:
    kind = "Mammal"                    # <- CLASS attribute     (shared by all)

    def __init__(self, name):
        self.name = name               # <- INSTANCE attribute  (its own)
```

---

### 4. Method —> *what the object DOES*

> A **method** is a function inside a class. It's the object's behavior.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):                   # <- METHOD: behavior
        return "..."
```

---

## Part 2: The 4 pillars

### 5. Inheritance —> *"is a"*

> A child class gets the attributes and methods of a parent class, for free.

```python
class Dog(Animal):                     # <- Dog INHERITS from Animal
    def __init__(self, name, breed):
        super().__init__(name)         # <- call the parent
        self.breed = breed             # <- add its own

d = Dog("Buddy", "Labrador")
print(d.name)                          # Buddy  <- came from Animal
```

A Dog **is an** Animal. That's the test for inheritance.

---

### 6. Polymorphism —> *same call, different result*

> The same method does something different depending on the object.

```python
class Dog(Animal):
    def speak(self): return "Woof"     # <- replaces the parent's version

class Cat(Animal):
    def speak(self): return "Meow"     # <- replaces the parent's version

for animal in [Dog("Buddy"), Cat("Luna")]:
    print(animal.speak())              # Woof / Meow
    #     ^ same call, different result
```

The loop doesn't know or care which class it's holding.

---

### 7. Encapsulation —> *hides the DATA*

> Keep the data safe inside the object. Nobody changes it directly.

```python
class Account:
    def __init__(self, balance):
        self._balance = balance        # <- "_" means: internal, don't touch

    @property
    def balance(self):                 # <- getter: how you READ it
        return self._balance

    @balance.setter
    def balance(self, value):          # <- setter: how you WRITE it (it CHECKS)
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

a = Account(1000)
print(a.balance)                       # 1000
a.balance = -50                        # ValueError <- the object protects itself
```

---

### 8. Abstraction —> *hides the COMPLEXITY*

> Show **what** it does. Hide **how** it does it.

```python
from abc import ABC, abstractmethod

class Animal(ABC):                     # <- ABSTRACT class
    @abstractmethod
    def speak(self): ...               # <- a rule: "you must write this"

class Dog(Animal):
    def speak(self): return "Woof"     # <- follows the rule

Animal()                               # TypeError <- you can't build this one
Dog()                                  # OK
```

Like driving a car: you use the wheel and the pedals. You don't need to know how the engine works.

---

## Cheat sheet

```
CLASS          -> the mold
OBJECT         -> what comes out of the mold
ATTRIBUTE      -> what it HAS          (data)
METHOD         -> what it DOES         (behavior)

INHERITANCE    -> reuses               ("is a")
POLYMORPHISM   -> varies               (same call, different result)
ENCAPSULATION  -> hides the DATA       (HOW)
ABSTRACTION    -> hides the COMPLEXITY (WHAT)
```

The first 4 are the **building blocks**.
The last 4 are the **pillars**.

---

## The 4 pillars in one sentence

> **Encapsulation** hides the data, **abstraction** hides the complexity,
> **inheritance** reuses code, and **polymorphism** lets the same call act differently.

Four verbs: **hides, hides, reuses, varies.**

---

## The only two people mix up

| | Hides | Question | Level |
|---|---|---|---|
| **Abstraction** | Complexity | **WHAT** do I show? | Design |
| **Encapsulation** | Data | **HOW** do I protect it? | Implementation |

Remember just this: **WHAT vs HOW.**

---

## Quick self-test

Cover the right column. Answer out loud.

| Question | Answer |
|---|---|
| What is OOP? | A way of writing code where everything is organized into objects that keep data and behavior together. |
| What is a class? | A blueprint that says what data and behavior its objects will have. |
| What is an object? | A real thing built from a class, with its own data. |
| What is an instance? | The same as an object, but said in relation to its class: "an instance **of** Animal". |
| Attribute vs method? | Attribute is what it **has** (data). Method is what it **does** (behavior). |
| Class vs instance attribute? | A class attribute is shared by everyone. An instance attribute belongs to one object. |
| What is inheritance? | A child class gets the attributes and methods of a parent class. Test: "is a". |
| What does `super()` do? | It calls the parent's version of a method, usually `__init__`. |
| What is polymorphism? | The same call does something different depending on the object. |
| What is encapsulation? | Keeping the data safe inside the object, so nobody changes it directly. |
| What is abstraction? | Showing what something does and hiding how it does it. |
| Abstraction vs encapsulation? | Abstraction hides complexity (**WHAT**). Encapsulation hides data (**HOW**). |
| Name the 4 pillars. | Encapsulation, abstraction, inheritance, polymorphism. |