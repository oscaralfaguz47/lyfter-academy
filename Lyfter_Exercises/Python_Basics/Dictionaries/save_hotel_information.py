print("----- Save Hotel Information -----")

hotel_info = {
    "name": "Tilajari Hotel",
    "number_of_stars": 4,
    "rooms": [
        {
            "room_number": 101,
            "floor": 1,
            "price_per_night": 95.0,
        },
        {
            "room_number": 102,
            "floor": 1,
            "price_per_night": 120.0,
        },
        {
            "room_number": 201,
            "floor": 2,
            "price_per_night": 150.0,
        },
    ]
}
print("Hotel Name:", hotel_info["name"])
print("Hotel rooms: ", hotel_info["rooms"])