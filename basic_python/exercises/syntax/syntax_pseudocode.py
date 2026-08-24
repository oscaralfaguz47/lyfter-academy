#First exercise 1.1 ----------------
price = float(input("Enter the price of the item: "))

discount = 0

if price < 100: 
    discount = price * 0.02
if price >= 100:
    discount = price * 0.10

print(f"The final price is: ${price - discount}, after a discount of ${discount}.")

#Second exercise 1.2 ----------------
num_of_seconds = float(input("Enter the number of seconds: "))

converted_minutes = num_of_seconds / 60

if converted_minutes < 10:
    print(f"{(10 * 60) - (num_of_seconds)} seconds less than 10 minutes.")
elif converted_minutes > 10:
    print(f"It's major than 10 minutes by {num_of_seconds - (10 * 60)} seconds.")
else:
    print("Exactly 10 minutes.")

#Third exercise 1.3 ----------------
n = int(input("Enter a number: "))

total_sum = 0
increasing_number = 0
for counter in range(1, n + 1):
    total_sum += counter
print(f"{total_sum}")