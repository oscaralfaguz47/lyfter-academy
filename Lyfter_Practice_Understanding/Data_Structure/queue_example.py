class Node:
    data: str
    next: "None"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Queue:
    def __init__(self):
        self.head = None

    def enqueue(self, data):
        new_node = Node(data)

        # Case 1, the line is empty, the new one is the first
        if self.head is None:
            self.head = new_node
            return

        # Case 2: The people are joining the line
        current_node = self.head
        while current_node.next is not None:
            current_node = current_node.next
        current_node.next = new_node

    def dequeue(self):
        if self.head is None:
            print("The line is empty, there are not people to take out")
            return None

        removed_node = self.head
        self.head = self.head.next
        removed_node.next = None
        return removed_node

    def print_structure(self):
        if self.head is None:
            print("Line empty")
            return

        current_node = self.head
        while current_node is not None:
            print(f"   -> {current_node.data}")
            current_node = current_node.next

queue = Queue()

print("--::: Step 1: People arrive in line :::-- ")
queue.enqueue("Oscar")
queue.enqueue("Maria")
queue.enqueue("Beto")
queue.print_structure()

print("--::: Step 2: We attend one person :::--")
attended = queue.dequeue()
print(f"Attended: {attended.data}")
queue.print_structure()

print(":::-- Step 3: We have a new person in the line :::--")
queue.enqueue("Diana")
queue.print_structure()

print("--::: We attend all the people in the line :::--")
while queue.head is not None:
    print(f"{queue.dequeue().data} was attended. ✓")
queue.print_structure()

print("---::: Trying to take off a person from an empty line :::---")
queue.dequeue()