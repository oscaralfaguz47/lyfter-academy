class Person:
    def __init__(self, name):
        self.name = name


class Bus:
    def __init__(self, max_passengers):
        self.max_passengers = max_passengers
        self.passengers_in_bus = []


    def add_passenger(self, person):
        if len(self.passengers_in_bus) < self.max_passengers:
            self.passengers_in_bus.append(person)
        else:
            print(
                f"The bus has reached its maximum passenger capacity. "
                f"{person.name} cannot board the bus."
                )

    def get_off_passenger(self, person):
        if person in self.passengers_in_bus:
            self.passengers_in_bus.remove(person)
        else:
            print(f"{person.name} is not on the bus")


def main():
    passenger1 = Person("Oscar")
    passenger2 = Person("Emilio")
    passenger3 = Person("Carlos")
    passenger4 = Person("Maria")
    passenger5 = Person("Enrique")
    passenger6 = Person("Carolina")

    my_bus = Bus(5)

    my_bus.add_passenger(passenger1)
    my_bus.add_passenger(passenger2)
    print(f"The bus has boarded ({len(my_bus.passengers_in_bus)}) passengers")
    print("Current passengers on the bus:")
    for passenger in my_bus.passengers_in_bus:
        print(passenger.name)

    my_bus.get_off_passenger(passenger1)
    print("The bus has dropped off (1) passenger")
    print(f"Current passengers on the bus: {len(my_bus.passengers_in_bus)}")
    for passenger in my_bus.passengers_in_bus:
        print(passenger.name)

    my_bus.add_passenger(passenger3)
    my_bus.add_passenger(passenger4)
    my_bus.add_passenger(passenger5)
    my_bus.add_passenger(passenger6)
    print("The bus has boarded (4) passengers")
    print(f"Current passengers on the bus: {len(my_bus.passengers_in_bus)}")
    for passenger in my_bus.passengers_in_bus:
        print(passenger.name)

    my_bus.add_passenger(passenger1)

    
if __name__ == "__main__":
    main()