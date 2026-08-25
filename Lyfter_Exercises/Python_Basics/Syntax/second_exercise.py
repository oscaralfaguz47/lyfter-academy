print("----- Verify number 30 -----")

number1 = int(input("Enter a number 1: "))
number2 = int(input("Enter a number 2: "))
number3 = int(input("Enter a number 3: "))

if number1 == 30 or number2 == 30 or number3 == 30:
    print("Correct")
elif number1 + number2 + number3 == 30:
    print("Correct")
else:
    print("Incorrect")

