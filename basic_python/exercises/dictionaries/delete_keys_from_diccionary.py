print("----- Delete keys from dictionary -----")

list_of_keys_to_remove = ['engine', 'fuel', 'model']
my_car = {
    'brand': 'Toyota',
    'engine': 3000,
    'fuel': 'Diesel',
    'model': 'Hilux',
    'year': 2024
}

for key in list_of_keys_to_remove:
    my_car.pop(key)

print("My car with removed keys: ", my_car)