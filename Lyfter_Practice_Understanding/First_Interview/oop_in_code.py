# A class is a blueprint from which objects are created.
from abc import ABC, abstractmethod

class MyAbstractParentClass(ABC):
    # ABSTRACTION with ABC and @abstractmethod 
    # Abstraction shows what a method does but hides how it does it, hiding the complexity
    # A class that inherits from ABC and has at least one @abstractmethod cannot be instantiated.
    @abstractmethod # This enforce child classes to implement this method 
    def my_abstracted_method(self):
        pass # Child classes have to implement the logic

class MyParentClass():
    # Class attributes: Variables that live in the class and are shared by all its instances. 
    # They can be accessed through the class or any object.
    PUBLIC_CONSTANT_ATTRIBUTE = {
        "name": "Constant class attribute",
        "description": "I'm a constant class attribute. By convention in Python, no one should change me."
    }

    public_normal_attribute = {
        "name": "Normal class attribute",
        "description": "I'm a normal class attribute, and I can be changed."
    }

    # __init__ runs automatically when an object is created and sets its initial instance attributes
    def __init__(
        self, 
        public_instance_parent_class_parameter, 
        protected_instance_parent_parameter,
        private_instance_parent_parameter
    ):
        # Instance attributes: Variables that live in an object (instance). Static methods can't access them.
        self.public_parent_instance_attribute = public_instance_parent_class_parameter

        # Assigned to the properties, so the setters validate the initial values too.
        self._protected_parent_instance_attribute = protected_instance_parent_parameter
        self.__private_parent_instance_attribute = private_instance_parent_parameter


    # ENCAPSULATION with @property and .setter
    # Encapsulation Keeps the data safe inside the object. The object control access to its own data.
    # Protected (_)and private (__) attributes shouldn't be accessed directly, only through properties or methods. In Python this is by convention:
    # _protect is just a signal, and __private uses name mangling (_MyParentClass__private...).
    @property # @property turns the method into a read-only attribute, controlling how a value is read.
    def protected_parent_instance_attribute(self):
        return self._protected_parent_instance_attribute

    @protected_parent_instance_attribute.setter # .setter defines how the property's value is changed, usually with validation
    def protected_parent_instance_attribute(self, new_value):
        if "protected" not in new_value["description"]:
            raise ValueError("The value must contain the word 'protected'")
        self._protected_parent_instance_attribute = new_value

    @property
    def private_parent_instance_attribute(self):
        return self.__private_parent_instance_attribute
    
    @private_parent_instance_attribute.setter
    def private_parent_instance_attribute(self, new_value):
        if "private" not in new_value["description"]:
            raise ValueError("The value must contain the word 'private'")
        self.__private_parent_instance_attribute = new_value

    # Methods are functions inside a class.
    
    # Instance method: receives the object (self)
    def my_instance_method(self):
        print(f"I'm an instance method, I receive the object, and I can use the object's attributes "
        f"like this: {self.public_parent_instance_attribute['name']} and the class attributes "
        f"like this: '{self.PUBLIC_CONSTANT_ATTRIBUTE['name']}'")

    # Class method: receives the class itself (cls).
    @classmethod
    def my_class_method(cls):
        print(f"I'm a class method, I receive the class itself, and I can only use class attributes "
        f"like this: '{cls.PUBLIC_CONSTANT_ATTRIBUTE['name']}', '{cls.public_normal_attribute['name']}'")

    # Static method: receives neither the object nor the class.
    @staticmethod
    def my_static_method():
        print("I'm a static method. I receive neither the object nor the class, "
        "so I cannot use instance attributes, only what I'm given as arguments.")

    # POLYMORPHISM 
    # The same method behaves differently depending on the objects's class.
    # Child classes override the parent method to provide their own version.
    def my_polymorphic_method(self):
        print("I'm the PARENT'S version of my_polymorphic_method(), and my child classes can override me.")


# INHERITANCE
# MyChildClass inherits from two classes: this is MULTI INHERITANCE.
# Python decides where to look for methods using the MRO (Method Resolution Order).
class MyChildClass(MyParentClass, MyAbstractParentClass):
    def __init__(
            self, 
            instance_parent_class_parameter,
            protected_instance_parent_parameter,
            private_instance_parent_parameter,
            instance_child_class_parameter
        ):

        # super () gives a child class access to its parent's methods.
        # super().__init__() runs the parent's constructor
        super().__init__(
            instance_parent_class_parameter, 
            protected_instance_parent_parameter,
            private_instance_parent_parameter
        )

        self.public_child_instance_attribute = instance_child_class_parameter

    # Overrides the parent's version (polymorphism)
    def my_polymorphic_method(self):
        print("I'm the CHILD'S version of the my_polymorphic_method(), I override my parent's.")

    # Overrides and extends the parent's version.
    def my_instance_method(self):
        super().my_instance_method() 
        print("I override my parent's method, reuse its behavior with super(), and add my own.")

    # Implements the abstract method required by MyAbstractParentClass.
    def my_abstracted_method(self):
        print("I'm implementing the logic of the my_abstract_method() that my parent MyAbstractParentClass doesn't implement.")


parent_class_instance_argument = {
    "name": "Parent class instance attribute",
    "description": "I'm an argument passed to the constructor. Oscar created me, and my whole value will "
    "be stored in the parent class instance attribute and the child classes will reuses me."
}

parent_class_protected_instance_argument = {
    "name": "Parent class PROTECTED instance attribute",
    "description": "I'm a protected argument passed to the constructor, but I cannot be accessed directly, only through my property."
}

parent_class_private_instance_argument = {
    "name": "Parent class PRIVATE instance attribute",
    "description": "I'm a private argument passed to the constructor, but I cannot be accessed directly, only through my property."
}

child_class_instance_argument = {
    "name": "Child class instance attribute",
    "description": "I'm an argument passed to the constructor. Oscar created me, and my whole value will "
    "be stored in the child class instance attribute."
}

child_class_protected_instance_argument = {
    "name": "Child class PROTECTED instance attribute",
        "description": "I'm a protected argument passed to the constructor, but I cannot be accessed directly, only through my property."
}

child_class_private_instance_argument = {
    "name": "Child class PRIVATE instance attribute",
        "description": "I'm a private argument passed to the constructor, but I cannot be accessed directly, only through my property."
}

# An object is an instance of a class
my_parent_object = MyParentClass(
    parent_class_instance_argument,
    parent_class_protected_instance_argument,
    parent_class_private_instance_argument
)

my_child_object = MyChildClass(
    parent_class_instance_argument, 
    child_class_protected_instance_argument,
    child_class_private_instance_argument,
    child_class_instance_argument
)

print("-------------- PARENT CLASS ------------------------")
print(f"I'm an object based on the class: {type(my_parent_object).__name__}")
my_parent_object.my_instance_method()
my_parent_object.my_class_method()
my_parent_object.my_instance_method()
print("")

print("-------------- CHILD CLASS (INHERITANCE) ------------------------")
print(f"I'm an object based on the class: {type(my_child_object).__name__}")
my_child_object.my_instance_method()
print(f"MRO: {[cls.__name__ for cls in MyChildClass.__mro__]}")
print("")

print("-------------- ABSTRACTION ------------------------")
my_child_object.my_abstracted_method()
try:
    MyAbstractParentClass()
except TypeError as error:
    print(f"Can't instantiate the abstract class: {error}")
print("")

print("-------------- POLYMORPHISM ------------------------")
for obj in [my_parent_object, my_child_object]:
    obj.my_polymorphic_method() # Same call, different behavior
print("")

print("-------------- ENCAPSULATION ------------------------")
# Reading through the properties
print(f"Read through the property: '{my_child_object.protected_parent_instance_attribute['name']}'")
print(f"Read through the property: '{my_child_object.private_parent_instance_attribute['name']}'")
# The setter rejects invalid values
try:
    my_child_object.protected_parent_instance_attribute = {
        "name": "Invalid value",
        "description": "This description doesn't have the keyword."
    }
except ValueError as error:
    print(f"Setter validation worked: {error}")

# The setter accepts valid value
my_child_object.protected_parent_instance_attribute = {
    "name": "Updated PROTECTED instance attribute",
    "description": "I was updated through the protected setter."
}
print(f"Updated through the setter: '{my_child_object.protected_parent_instance_attribute["name"]}'")

# Private attributes can't be accessed directly from outside the class
try:
    print(my_child_object.__private_parent_instance_attribute)
except AttributeError:
    print("Direct access to the private attribute failed, as expected.")