from abc import ABC, abstractmethod
from math import pi

class Shape(ABC):

    @abstractmethod
    def calculate_perimeter(self):
        pass

    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def calculate_perimeter(self):
        return 2 * pi * self.radius

    def calculate_area(self):
        return pi * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def calculate_perimeter(self):
        return 4 * self.side
    
    def calculate_area(self):
        return self.side * self.side

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_perimeter(self):
        return (self.width + self.height) * 2
    
    def calculate_area(self):
        return self.width * self.height

shapes = [Circle(50), Square(10), Rectangle(10, 50)]

for shape in shapes:
    name = type(shape).__name__
    print(f"{name}: perimeter = {shape.calculate_perimeter():.2f}, area = {shape.calculate_area():.2f}")

