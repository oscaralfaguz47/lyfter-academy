class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise ValueError("The salary cannot be a negative value.")
        self.name = name
        self.salary = salary

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("The name cannot be empty.")
        self._name = value

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("The salary cannot be a negative value.")
        self._salary = value

    def promote(self, percentage_increase):
        self._salary += self._salary * percentage_increase

employee = Employee("Oscar Alfaro", 5000)
employee.promote(0.05)
print(employee.salary)