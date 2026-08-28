class Node: 
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

    def push_right(self, data):
        new_node = Node(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def pop_left(self):
        if self.head is None:
            print("The deque is empty")
            return None

        removed_node = self.head
        self.head = removed_node.next

        if self.head is None: # If the Deque is totally empty we have to let the tail go
            self.tail = None
        else:
            self.head.prev = None

        removed_node.next = None
        return removed_node

    def pop_right(self):
        if self.tail is None:
            print("The Dequeue is empty")
            return None

        removed_node = self.tail
        self.tail = removed_node.prev

        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        removed_node.prev = None
        return removed_node

    def print_structure(self):
        if self.head is None:
            print("(Deque is empty)")
            return

        current_node = self.head
        while current_node is not None:
            print(f"  ({current_node.data})")
            current_node = current_node.next

    def print_backwards(self):
        current_node = self.tail
        while current_node is not None:
            print(f" ({current_node.data})")
            current_node = current_node.prev

deque = Deque()

print("--::: I add tortillas :::--")
deque.push_right("Tortilla B")
deque.push_right("Tortilla C")
deque.push_left("Tortilla A")
deque.print_structure()

print("--::: De same bag of Tortillas read backwards :::--")
deque.print_backwards()

print("--::: I take a tortilla from the bottom of the bag :::--")
print(f"I took: {deque.pop_right().data}")
deque.print_structure()

print("--::: I take a tortilla from the top of the bag :::--")
print(f"I took: {deque.pop_left().data}")
deque.print_structure()

print("--::: I eat the last one :::--")
print(f"I took: {deque.pop_left().data}")
deque.print_structure()
print(f"head = {deque.head}, tail = {deque.tail}")

print("--::: I fill the bag again :::--")
deque.push_left("New Tortilla")
deque.print_structure()
print(f"head data = {deque.head.data}, tail data = {deque.tail.data}")