from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def browse_the_internet(self):
        pass

class TouchScreenMixin:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calculate_screen_area(self):
        return self.width * self.height

class MemoryCapacityMixin:
    def __init__(self, total_memory_gb):
        self.total_memory_gb = total_memory_gb
        self.used_memory_gb = 0

    def get_free_memory(self):
        return self.total_memory_gb - self.used_memory_gb

    def use_memory(self, amount_gb):
        if amount_gb > self.get_free_memory():
            raise ValueError(
                f"Not enough memory: {self.get_free_memory()} GB free, "
                f"tried to use {amount_gb} GB"
            )
        self.used_memory_gb += amount_gb

class Phone(Device, TouchScreenMixin, MemoryCapacityMixin): 
    def __init__(self, name, model, screen_with, screen_height, total_memory_gb):
        Device.__init__(self, name)
        TouchScreenMixin.__init__(self, screen_with, screen_height)
        MemoryCapacityMixin.__init__(self, total_memory_gb)
        self.model = model

    def browse_the_internet(self):
        print(f"{self.model} opens the browser and connects to the internet.")
    

phone = Phone("Samsung", "Galaxy S", 6, 3, 220)
phone.browse_the_internet()
print(f"Screen area: {phone.calculate_screen_area()}")
phone.use_memory(100)
phone.use_memory(10)
print(f"Now the phone has: {phone.used_memory_gb} GB of used memory.")