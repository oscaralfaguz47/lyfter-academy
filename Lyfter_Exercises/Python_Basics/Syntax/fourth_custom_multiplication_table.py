print("----- Custom Multiplication Table -----")

number = int(input("Enter a number from 1 to 10: "))

for i in range(1, 13):
    print(f"{number} x {i} = {number * i}")