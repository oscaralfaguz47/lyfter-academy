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

        # The line is empty, the new node is the first one
        if self.head is None:
            self.head = new_node
            return

        # The line has nodes, we put the new one at the end

        current_node = self.head
        while current_node.next is not None:
            current_node = current_node.next

        current_node.next = new_node

    def dequeue(self):
        if self.head is None:
            print("The line is empty")
            return None

        removed_node = self.head
        self.head = self.head.next
        removed_node.next = None
        return removed_node

    def print_all(self):
        if self.head is None:
            print("The line is empty")
            return

        result = ""
        current_node = self.head
        while current_node is not None:
            result += current_node.data
            current_node = current_node.next
            if current_node is not None:
                result += " -> "
        print(result)

q = Queue()

q.enqueue("A")
q.enqueue("B")
q.enqueue("C")

q.print_all()

removed_node = q.dequeue()
print(removed_node.data)
q.print_all()