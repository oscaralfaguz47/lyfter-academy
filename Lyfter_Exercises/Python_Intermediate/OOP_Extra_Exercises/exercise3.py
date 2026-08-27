class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self):
        self.list_of_products = []

    def add_product(self, product):
        self.list_of_products.append(product)

    def show_all_products(self):
        print("# List of all products ---")
        for product in self.list_of_products:
            print(f"{product.name}, {product.quantity}, {product.price}")

    def calculate_total_value_of_inventory(self):
        total_value = 0
        for product in self.list_of_products:
            total_value += product.quantity * product.price
        return total_value

product1 = Product("Keyboard", 15000, 2)
product2 = Product("Speaker", 20000, 3)

my_inventory = Inventory()
my_inventory.add_product(product1)
my_inventory.add_product(product2)

my_inventory.show_all_products()
print(my_inventory.calculate_total_value_of_inventory())