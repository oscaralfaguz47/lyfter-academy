import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return math.pi * self.radius ** 2


circle1 = Circle(50)
circle2 = Circle(5)
circle3 = Circle(20)

print(
    f"The areas of the circles are: "
    f"Circle 1: {circle1.get_area():.2f}, "
    f"Circle 2: {circle2.get_area():.2f}, "
    f"Circle 3: {circle3.get_area():.2f}"
    )

