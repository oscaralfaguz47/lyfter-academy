class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)

        if self.root is None:
            self.root = new_node
            return
        current_node = self.root
        while True:
            if data < current_node.data:
                if current_node.left is None:   # There's an space, we save it here
                    current_node.left = new_node
                    return
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.right = new_node
                    return
                current_node = current_node.right

    def contains(self, data):
        current_node = self.root
        while current_node is not None:
            if data == current_node.data:
                return True
            if data < current_node.data:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return False

    def print_structure(self):
        self.print_node(self.root)

    def print_node(self, node):
        if node is None:
            return
        self.print_node(node.left)   # 1. All the left
        print(f" {node.data}")       # 2. Me
        self.print_node(node.right)  # 3. All the right

    def print_tree(self, node="start", level=0):
        if node == "start":
            node = self.root
        if node is None:
            return
        self.print_tree(node.right, level + 1)
        print("  " * level + str(node.data))
        self.print_tree(node.left, level + 1)


tree = BinaryTree()

print("--::: I insert: 50, 30, 70, 20, 40, 60, 80 :::--")
for value in [50, 30, 70, 20, 40, 60, 80]:
    tree.insert(value)

print("--::: Shape of the tree (turn the head left): :::--")
tree.print_tree()

print("Route in-order (print ordered):")
tree.print_structure()

print("--::: Searching :::--")
print(f"contains(40) -> {tree.contains(40)}")
print(f"contains(45) -> {tree.contains(45)}")

print("--::: Accessing manually :::--")
print(f"root: {tree.root.data}")
print(f"root.left: {tree.root.left.data}")
print(f"root.left.right: {tree.root.left.right.data}")