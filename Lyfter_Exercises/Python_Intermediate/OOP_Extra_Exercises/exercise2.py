class Animal:
    def __init__(self, name):
        self.name = name
        pass

    def speak(self):
        return "Makes a sound"

class Dog(Animal):
    def speak(self):
        return "Guau"

class Cat(Animal):
    def speak(self):
        return "Miau"


my_dog = Dog("Firulais")
my_cat = Cat("Ripple")
animal = Animal("An animal")
print(f"{my_dog.name} goes {my_dog.speak()}")
print(f"{my_cat.name} goes {my_cat.speak()}")
print(f"{animal.name} {animal.speak()}")