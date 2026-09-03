class Node:
    data: str
    next: "Node"
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node   

    def prepend(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node        

    def delete(self, data):
        current_node = self.head

        while current_node is not None:
            if current_node.data == data:
                if current_node.prev is None:
                    self.head = current_node.next
                else:
                    current_node.prev.next = current_node.next

                if current_node.next is None:
                    self.tail = current_node.prev
                else:
                    current_node.next.prev = current_node.prev
                current_node.prev = None
                current_node.next = None
                return
            current_node = current_node.next
        print(f"{data} is not in the list")
        return

    def print_forward(self):
        if self.head is None:
            print("The list is empty")
            return
        
        result = ""
        current_node = self.head
        while current_node is not None:
            result += current_node.data
            if current_node.next is not None:
                result += " -> "
            current_node = current_node.next
        print(result)

    def print_backward(self):
        if self.tail is None:
            print("The list is empty")
            return

        result = ""
        current_node = self.tail
        while current_node is not None:
            result += str(current_node.data)
            if current_node.prev is not None:
                result += " -> "
            current_node = current_node.prev
        print(result)
        

dll = DoubleLinkedList()
dll.append("A")
dll.append("B")
dll.append("C")
dll.print_forward()
dll.print_backward()

dll.prepend("X")
dll.print_forward()
dll.print_backward()

dll.delete("B")
dll.print_forward()
dll.print_backward()