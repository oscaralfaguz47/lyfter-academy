from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, year):
        self._brand = brand
        self._year = year

    def get_info(self):
        return f"{self._brand} ({self._year})"

class Car(Vehicle):
    def __init__(self, brand, year, num_of_doors):
        super().__init__(brand, year)
        self.num_of_doors = num_of_doors

    def get_info(self):
        return f"{super().get_info()}, num of doors {self.num_of_doors}"

class Motorcycle(Vehicle):
    def __init__(self, brand, year, motorcycle_type):
        super().__init__(brand, year)
        self.motorcycle_type = motorcycle_type

    def get_info(self):
        return f"{super().get_info()}, motorcycle type: {self.motorcycle_type}"


vehicle1 = Car("Toyota", 2024, 4)
vehicle2 = Motorcycle("Honda", 2023, "Enduro")

print(vehicle1.get_info())
print(vehicle2.get_info())