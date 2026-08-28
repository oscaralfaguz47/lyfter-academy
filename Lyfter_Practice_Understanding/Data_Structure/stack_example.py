class Node:
    data: str
    next: "None"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data) 
        new_node.next = self.top # The new node points to the old one
        self.top = new_node      # Now the new node is the top

    def pop(self):
        if self.top is None:
            print("The stack is empty, there are nothing to take out")
            return None

        removed_node = self.top
        self.top = self.top.next
        removed_node.next = None
        return removed_node

    def peek(self): # Take the top node if there's one
        if self.top is None:
            return None
        return self.top.data

    def print_structure(self):
        if self.top is None:
            print("The stack is empty")
            return

        current_node = self.top
        while current_node is not None:
            print(f" [{current_node.data}]")
            current_node = current_node.next

stack = Stack()

print("--::: Stack the plates :::--")
stack.push("Plate 1")
stack.push("Plate 2")
stack.push("Plate 3")
stack.print_structure()

print(f"-The plate on the top is: {stack.peek()}")

print("--::: I wash the top plate :::--")
washed = stack.pop()
print(f"- Washed plate: {washed.data}")
stack.print_structure()

print("--::: I have a new dirty plate in the stack :::--")
stack.push("Plate 4")
stack.print_structure()

print("--::: I wash all the plates :::--")
while stack.top is not None:
    print(f"- Washed plate: {stack.pop().data}")
stack.print_structure()

print("--::: Take off a node from an empty stack :::--")
stack.pop()