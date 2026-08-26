class Rectangle:
    def __init__(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("The width and height cannot be negative numbers.")
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return (self.width + self.height) * 2


while True:
    try:
        rectangle_width = float(input("Enter the width: "))
        rectangle_height = float(input("Enter the height: "))
        my_rectangle = Rectangle(rectangle_width, rectangle_height)
    except ValueError as e:
        print(e)
    else:
        break

print(my_rectangle.get_area())
print(my_rectangle.get_perimeter())
