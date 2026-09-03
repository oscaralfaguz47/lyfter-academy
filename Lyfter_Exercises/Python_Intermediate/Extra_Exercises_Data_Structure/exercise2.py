class Node:
    data: str
    next: "Node"
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_back(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current_node = self.head
        while current_node.next is not None:  # Walk until the last one
            current_node = current_node.next
        current_node.next = new_node

    def delete(self, data):
        if self.head is None:
            print("The list is empty")
            return
        
        if self.head.data == data:
            self.head = self.head.next
            return

        previous_node = self.head
        current_node = self.head.next

        while current_node is not None:
            if current_node.data == data:
                previous_node.next = current_node.next
                current_node.next = None
                return
            previous_node = current_node
            current_node = current_node.next
        

    def print_all(self):
        if self.head is None:
            print("The list is empty")
            return

        result = ""
        current_node = self.head
        while current_node is not None:
            result += str(current_node.data)
            if current_node.next is not None:
                result += " -> "
            current_node = current_node.next
        print(result)    

ll = LinkedList()

ll.insert_front(10)
ll.insert_front(20)
ll.print_all()

ll.insert_back(30)
ll.print_all()

ll.delete(10)
ll.print_all()




        
