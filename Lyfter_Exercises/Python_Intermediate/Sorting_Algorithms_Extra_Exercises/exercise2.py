class Node:
    data: str
    next: "Node"

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

    def bubble_sort_steps(self):
        if self.top is None:
            return 0, 0

        changes_made = True
        num_changes_made = 0
        num_iterations = 0
        while changes_made:
            changes_made = False
            num_iterations += 1
            current_node = self.top
            while current_node.next is not None:
                next_node = current_node.next

                if current_node.data > next_node.data:
                    temp = current_node.data
                    current_node.data = next_node.data
                    next_node.data = temp
                    changes_made = True
                    num_changes_made += 1
                current_node = current_node.next
        return num_iterations, num_changes_made

stack = Stack()

print("--::: MY STACK :::--")
stack.push("55")
stack.push("20")
stack.push("15")
stack.push("50")
stack.print_structure()
iterations, exchanges = stack.bubble_sort_steps()
print("--- Ordered list ---")
stack.print_structure()
print(f"Iterations: {iterations}")
print(f"Exchanges: {exchanges}")

