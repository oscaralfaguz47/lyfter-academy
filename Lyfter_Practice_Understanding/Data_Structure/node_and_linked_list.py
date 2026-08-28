class Node:
    data: str
    next: "Node"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    head: Node

    def __init__(self, head=None):
        self.head = head

    def print_structure(self):
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next

    def get_last(self):
        current = self.head
        if current is None:
            return None
        while current.next is not None:
            current = current.next
        return current 


#We create the nodes from back to to front
third_node = Node("I'm the third node")
second_node = Node("I'm the second node", third_node)
first_node = Node("I'm the first node", second_node)

linked_list = LinkedList(first_node)

print("---- Browsing the list ----")
linked_list.print_structure()

print("-- The last node --")
last = linked_list.get_last()
print(last.data)

print("-- Accessing manually without while --")
print(linked_list.head.data)
print(linked_list.head.next.data)
print(linked_list.head.next.next.data)
print(linked_list.head.next.next.next)

print("-- An empty list --")
empty_list = LinkedList()
empty_list.print_structure()
print(f"get_last() -> {empty_list.get_last()}")

print("\n== References: are the SAME object ==")
print(f"first_node.next es second_node? {first_node.next is second_node}")
second_node.data = "I have been changed the name"
linked_list.print_structure()