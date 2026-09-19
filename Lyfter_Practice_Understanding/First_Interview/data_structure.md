# Data Structures

The 5 topics: **Linked List, Queue, Stack, Double Ended Queue, Binary Tree.**

The first four are **linear** (one item after another).
The last one is **hierarchical** (branches).

---

# 1. Linked List

> A **linked list** is a chain of **nodes**. Each node holds a value and a **link to the next node**.

The items are **not** next to each other in memory. They are tied together by links.

```
head                                   tail
 |                                      |
 v                                      v
[1|->] --> [2|->] --> [3|->] --> None
```

## The types

| Type | What each node has |
|---|---|
| **Singly linked** | `next` only -> you can go forward |
| **Doubly linked** | `next` and `prev` -> you can go both ways |
| **Circular** | The last node points back to the first |

## The code

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push_right(self, value):          # add at the end -> O(1)
        node = Node(value)
        if self.head is None:             # EDGE CASE: empty list
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node         # <- connect .next here, not .prev again
            self.tail = node
        self.size += 1

    def push_left(self, value):           # add at the front -> O(1)
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def pop_right(self):                  # remove from the end -> O(1)
        if self.tail is None:             # EDGE CASE: empty
            return None
        node = self.tail
        self.tail = node.prev
        if self.tail is None:             # EDGE CASE: it just became empty
            self.head = None
        else:
            self.tail.next = None
        self.size -= 1
        return node.value

    def pop_left(self):                   # remove from the front -> O(1)
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self.size -= 1
        return node.value

    def find(self, value):                # search -> O(n)
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def __iter__(self):                   # lets you use for and list()
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self):
        return self.size
```

## The 3 bugs that happen every single time

| Bug | What you see |
|---|---|
| Forgetting the **empty list** case | `AttributeError: 'NoneType' object has no attribute 'next'` |
| In `push_right`, writing `.prev` twice instead of `.next` | Going backwards works, going forwards is broken |
| Forgetting the **"it became empty"** case in `pop` | `head` still points to a node you removed |

The habit that prevents all three: before writing any insert or remove, ask **"what if there are zero items? what if there is exactly one?"**

## Speed vs a normal list

| Operation | Linked List | Python `list` |
|---|---|---|
| Get item number 5 | **O(n)** | **O(1)** |
| Add/remove at the **front** | **O(1)** | **O(n)** |
| Add/remove at the **end** | O(1) | O(1) |
| Search | O(n) | O(n) |
| Memory | Extra link per node, scattered | All together |

**The trade in one line:** a normal list gives you fast access by position but slow inserts at the front. A linked list gives you the opposite.

## Do you ever use it?

Almost never in Python. `list` covers most cases and `collections.deque` covers the rest, and both are written in C. It shows up in interviews because it tests whether you can handle links and edge cases.

In C# this is `LinkedList<T>` — same structure, same trade-offs.

---

# 2. Queue

> A **queue** is **FIFO**: *First In, First Out*. The first one in is the first one out.

You add at one end and remove from the other.

```
   remove <--  [1][2][3][4]  <-- add
              front       back
```

**Picture it:** the line at the bank. First to arrive, first to be served.

## The operations

| Operation | What it does | Speed |
|---|---|---|
| `enqueue` | Add at the back | O(1) |
| `dequeue` | Remove from the front | O(1) |
| `peek` | Look at the front, don't remove | O(1) |
| `is_empty` | Is it empty? | O(1) |

## The code

```python
from collections import deque


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)          # O(1)

    def dequeue(self):
        if self.is_empty():               # EDGE CASE: empty queue
            raise IndexError("Queue is empty")
        return self._items.popleft()      # O(1)

    def peek(self):
        return self._items[0] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


q = Queue()
q.enqueue("A")
q.enqueue("B")
print(q.dequeue())      # A  <- the first one in
```

## Why `deque` and not a list — the key point

```python
items = []
items.append("A")       # O(1)  fine
items.pop(0)            # O(n)  BAD
```

`list.pop(0)` is **O(n)** because a list sits in one block of memory. Removing the first item forces Python to move every other item one step left.

`deque` is a chain of blocks, so `popleft()` is **O(1)** — it just moves the head pointer.

With 1,000,000 items, emptying a list-based queue costs O(n²). With a deque it's O(n).

## The variants

| Type | What it does |
|---|---|
| **Simple queue** | Plain FIFO |
| **Circular queue** | Fixed size, reuses the freed slots |
| **Priority queue** | Serves by priority, not by arrival — `heapq` |
| **Deque** | Add and remove at both ends |

```python
import heapq

tasks = []
heapq.heappush(tasks, (2, "medium"))
heapq.heappush(tasks, (1, "urgent"))
heapq.heappush(tasks, (3, "low"))
print(heapq.heappop(tasks))     # (1, 'urgent')  <- lowest number first
```

## For threads

```python
from queue import Queue         # NOT collections.deque

q = Queue()
q.put("task")                   # thread-safe
item = q.get()
```

`collections.deque` is fast but you handle the locking. `queue.Queue` already includes it.

## Where it's used in real life

- **BFS** — going through a tree or graph level by level
- **Task queues** — Celery, RabbitMQ, Azure Service Bus
- Print queues, request buffers, rate limiting
- Producer / consumer between threads

In C#: `Queue<T>` with `Enqueue()`, `Dequeue()`, `Peek()`.

---

# 3. Stack

> A **stack** is **LIFO**: *Last In, First Out*. The last one in is the first one out.

You add and remove from the **same end**, called the top.

```
     add |  ^ remove
         v  |
        [3]  <- top
        [2]
        [1]  <- bottom
```

**Picture it:** a pile of plates. You put one on top, you take one from the top.

## The operations

| Operation | What it does | Speed |
|---|---|---|
| `push` | Add on top | O(1) |
| `pop` | Remove from the top and return it | O(1) |
| `peek` | Look at the top, don't remove | O(1) |
| `is_empty` | Is it empty? | O(1) |

## The code

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)          # O(1)

    def pop(self):
        if self.is_empty():               # EDGE CASE: empty stack
            raise IndexError("Stack is empty")
        return self._items.pop()          # O(1) -> removes the LAST one

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


s = Stack()
s.push("A")
s.push("B")
print(s.pop())      # B  <- the last one in
```

## Here a normal list IS fine — and that's the contrast

```python
stack = []
stack.append(x)     # push -> O(1)
stack.pop()         # pop  -> O(1), removes from the END
```

| | Stack | Queue |
|---|---|---|
| Works on | The **end** of the list | **Both** ends |
| Is a plain list fine? | **Yes** | **No** |
| Why | `append` and `pop()` are both O(1) | `pop(0)` is O(n) |

Both operations happen at the end of the list, and the end is exactly where a list is cheap. Nothing has to move.

## The classic exercise: balanced brackets

If they ask about stacks, this is probably the exercise.

```python
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
    return len(stack) == 0          # it must end empty

print(is_balanced("{[()]}"))        # True
print(is_balanced("{[(])}"))        # False
print(is_balanced("(("))            # False  <- leftovers in the stack
```

Two edge cases the easy version misses: a closing bracket with an **empty stack**, and **leftover** open brackets at the end.

## Where it's used in real life

- **The call stack** — how the language keeps track of function calls. Endless recursion fills it up: `RecursionError: maximum recursion depth exceeded` (Python's limit is 1000).
- **Undo / redo** in editors
- **The browser back button**
- **DFS** — going deep first
- Checking brackets, evaluating expressions, backtracking

## Stack and recursion are the same idea

Any recursive function can be rewritten with a stack. Recursion just uses the language's **hidden** stack.

```python
# Recursive DFS
def dfs(node):
    if node is None: return
    print(node.value)
    dfs(node.left)
    dfs(node.right)

# The same thing with your own stack
def dfs_loop(root):
    if root is None: return
    stack = [root]
    while stack:
        node = stack.pop()
        print(node.value)
        if node.right: stack.append(node.right)    # right in first...
        if node.left:  stack.append(node.left)     # ...so left comes out first
```

In C#: `Stack<T>` with `Push()`, `Pop()`, `Peek()`.

---

# 4. Double Ended Queue (Deque)

> A **deque** (say "deck") lets you add and remove at **both ends** in O(1).
> It can act as a stack **and** as a queue.

```
appendleft ->  [1][2][3][4]  <- append
   popleft <--                --> pop
```

## The operations

| Operation | End | Speed |
|---|---|---|
| `append(x)` | Right | O(1) |
| `appendleft(x)` | Left | O(1) |
| `pop()` | Right | O(1) |
| `popleft()` | Left | O(1) |
| `d[i]` (middle) | — | **O(n)** |

## The code

```python
from collections import deque

d = deque([1, 2, 3])
d.append(4)             # [1, 2, 3, 4]      right
d.appendleft(0)         # [0, 1, 2, 3, 4]   left
d.pop()                 # 4
d.popleft()             # 0
d.rotate(1)             # rotate right (negative = left)
d.extendleft([9, 8])    # careful: goes in BACKWARDS -> [8, 9, 1, 2, 3]
```

## `maxlen` — the feature worth remembering

```python
last_three = deque(maxlen=3)
for n in range(6):
    last_three.append(n)

print(last_three)       # deque([3, 4, 5], maxlen=3)
```

When it's full, adding on one end **throws away** from the other end automatically.
A "last N items" buffer with zero extra code.

## It can be both

```python
# As a STACK (LIFO) -> both operations on the right
stack = deque()
stack.append(x)
stack.pop()

# As a QUEUE (FIFO) -> add right, remove left
queue = deque()
queue.append(x)
queue.popleft()
```

This is why `deque` is the one to remember: it covers both patterns, always O(1).

## How it's built

Not a plain block of memory and not a plain linked list. It's a **chain of small blocks** (about 64 items each).

That design is why both ends are O(1), but **getting the item in the middle is O(n)** — Python has to walk block by block.

## deque vs list

| Operation | `deque` | `list` |
|---|---|---|
| Add/remove at the **end** | O(1) | O(1) |
| Add/remove at the **front** | **O(1)** | **O(n)** |
| Get by position | **O(n)** | **O(1)** |
| Slicing `[1:3]` | not supported | yes |

**The rule:** working on the ends -> `deque`. Need positions or slicing -> `list`.

## Where it's used in real life

- **Sliding window** problems — moving average, max in a window
- **Last N items** — recent logs, command history
- **Undo / redo** — undo from one end, redo from the other
- **BFS** — the queue used to walk a tree
- Checking if a word reads the same backwards

```python
def is_palindrome(text):
    d = deque(text.lower().replace(" ", ""))
    while len(d) > 1:
        if d.popleft() != d.pop():      # compare both ends, move inward
            return False
    return True
```

## For threads

`append` and `popleft` are atomic, so a deque is safe for simple producer/consumer. For waiting and timeouts, use `queue.Queue` — which is built on a deque anyway.

In C#: there is no built-in deque. `Queue<T>` and `Stack<T>` are separate. `LinkedList<T>` is the closest.

---

# 5. Binary Tree

> A **binary tree** is a structure with branches, where each node has **at most two children**: `left` and `right`.

```
        50          <- root
       /  \
     30    70
    /  \   / \
   20  40 60  80    <- leaves
```

## The words

| Word | Meaning |
|---|---|
| **Root** | The top node. No parent. |
| **Leaf** | A node with no children. |
| **Height** | Longest path from a node down to a leaf. |
| **Depth** | Distance from the root down to a node. |
| **Subtree** | Any node plus everything under it. |

## Binary Tree vs Binary Search Tree — the key difference

| | Rule |
|---|---|
| **Binary Tree** | Only this: max two children. No order. |
| **BST** (Binary **Search** Tree) | Plus: **everything on the left is smaller, everything on the right is bigger.** |

That order rule is what makes searching **O(log n)**: at every node you throw away half the tree. Without it you would have to check every node, O(n).

## The code

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:              # EDGE CASE: empty tree
            self.root = TreeNode(value)
            return
        self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)
        # equal value -> ignored, no duplicates

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False                   # base case: not found
        if value == node.value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def height(self, node):
        if node is None:
            return -1                      # an empty tree has height -1
        return 1 + max(self.height(node.left), self.height(node.right))
```

Every method follows the same shape: **base case** (`node is None`), then go left or go right. That's why trees are the natural place to practice recursion.

## The 4 ways to walk a tree

**Depth first (goes deep), using recursion:**

```python
def in_order(node, result=None):        # LEFT -> ROOT -> RIGHT
    if result is None:
        result = []
    if node:
        in_order(node.left, result)
        result.append(node.value)
        in_order(node.right, result)
    return result


def pre_order(node, result=None):       # ROOT -> LEFT -> RIGHT
    if result is None:
        result = []
    if node:
        result.append(node.value)
        pre_order(node.left, result)
        pre_order(node.right, result)
    return result


def post_order(node, result=None):      # LEFT -> RIGHT -> ROOT
    if result is None:
        result = []
    if node:
        post_order(node.left, result)
        post_order(node.right, result)
        result.append(node.value)
    return result
```

**Breadth first (level by level), using a queue:**

```python
from collections import deque

def level_order(root):
    if root is None:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left:  queue.append(node.left)
        if node.right: queue.append(node.right)
    return result
```

**On the tree drawn above:**

| Walk | Result | What it's for |
|---|---|---|
| **In-order** | `[20, 30, 40, 50, 60, 70, 80]` | **Comes out SORTED** |
| **Pre-order** | `[50, 30, 20, 40, 70, 60, 80]` | Copying / saving a tree |
| **Post-order** | `[20, 40, 30, 60, 80, 70, 50]` | Deleting a tree (children first) |
| **Level-order** | `[50, 30, 70, 20, 40, 60, 80]` | BFS, printing level by level |

**The one to memorize: in-order on a BST gives you the values in order.** That is the most asked fact about trees.

The names are a hint: **pre / in / post** tells you **when you visit the root** compared to the children.

**And notice how everything connects:**

```
DFS  ->  uses a STACK  (the hidden one, through recursion)
BFS  ->  uses a QUEUE
```

## Speed

| Operation | Balanced | Degenerate (worst case) |
|---|---|---|
| Search | **O(log n)** | **O(n)** |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Walk it all | O(n) | O(n) |

## The worst case — the follow-up question

```python
for value in [1, 2, 3, 4, 5]:     # inserted already in order
    tree.insert(value)
```

```
1
 \
  2
   \
    3
     \
      4
```

Every node goes right. The tree turns into a **linked list**. The height becomes n and everything drops to **O(n)** — you lost the whole advantage.

That is why **self-balancing trees** exist: **AVL** and **Red-Black** trees rotate when you insert, keeping the height at O(log n).

Worth knowing: Java's `TreeMap` and .NET's `SortedDictionary` are Red-Black trees. And **B-trees** (same idea, more children per node) are what database indexes use. When you create an index on a column in SQL Server, you're building one of these.

## The types of binary tree

| Type | Meaning |
|---|---|
| **Full** | Every node has 0 or 2 children |
| **Complete** | Every level full except maybe the last, filled left to right |
| **Perfect** | All leaves at the same level |
| **Balanced** | The two sides differ in height by 1 at most |
| **Degenerate** | One child each — basically a linked list |

## Why use a BST if a dict is O(1)?

Fair question. The answer: a BST keeps things **in order**. It gives you sorted output, range questions ("all values between 30 and 60"), min and max, and "what comes next" — none of which a dict can do.

You trade O(1) lookup for O(log n) lookup **plus** order.

---

# Cheat sheet

```
LINKED LIST  -> nodes joined by links
                Front/end: O(1)   |   By position: O(n)
                Watch the empty list case

QUEUE        -> FIFO, first in first out       (the bank line)
                Use deque, NOT list, because pop(0) is O(n)

STACK        -> LIFO, last in first out        (a pile of plates)
                A plain list is fine here
                The call stack is one

DEQUE        -> both ends, both O(1)
                Acts as a stack AND a queue
                maxlen = keep only the last N

BINARY TREE  -> max 2 children
                BST adds: left smaller, right bigger -> O(log n)
                IN-ORDER comes out SORTED
                Inserted in order -> becomes a list -> O(n)
```

## How they link together

```
Linked list  ->  is what a deque is made of
Deque        ->  is what you build a queue with
Queue        ->  is what BFS uses
Stack        ->  is what DFS uses (through recursion)
```

---

# Quick self-test

Cover the right column. Answer out loud.

| Question | Answer |
|---|---|
| What is a linked list? | A chain of nodes, where each node holds a value and a link to the next one. |
| Why is there no access by position? | The nodes are not next to each other in memory, so you have to walk the chain: O(n). |
| What does a linked list win at? | Adding or removing at the front: O(1), while a normal list is O(n). |
| Singly vs doubly linked? | Singly has `next` only. Doubly also has `prev`, so you can go both ways. |
| What bug always appears? | Not handling the empty list, or the list becoming empty after a removal. |
| What is a queue? | FIFO: the first one in is the first one out. |
| Why not use a list for a queue? | `list.pop(0)` is O(n) because every other item has to shift. `deque.popleft()` is O(1). |
| What is a stack? | LIFO: the last one in is the first one out. |
| Is a list fine for a stack? | Yes. `append` and `pop()` both work at the end, both O(1). |
| Name a real stack. | The call stack. That's why endless recursion gives a `RecursionError`. |
| Stack vs queue in one line? | Stack: same end, LIFO, DFS. Queue: opposite ends, FIFO, BFS. |
| What is a deque? | A queue where you can add and remove at both ends, all O(1). |
| What does `maxlen` do? | When it's full, adding on one end drops an item from the other end automatically. |
| Weak spot of a deque? | Getting an item in the middle is O(n), and no slicing. |
| Binary tree vs BST? | A binary tree just limits you to 2 children. A BST also keeps smaller on the left, bigger on the right. |
| Why is a BST O(log n)? | At every node you throw away half of what's left. |
| Name the 4 walks. | In-order, pre-order, post-order, level-order. |
| Which one comes out sorted? | In-order, on a BST. |
| What does level-order use? | A queue. It's BFS. |
| What is the worst case of a BST? | Inserting already-sorted values. It becomes a linked list and drops to O(n). |
| How is that fixed? | Self-balancing trees: AVL and Red-Black. |
| Why a BST instead of a dict? | A dict is O(1) but has no order. A BST gives you sorted output, ranges, min and max. |