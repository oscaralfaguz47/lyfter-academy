print("----- Temperature unit converter -----")

temperature = float(input("Enter a Celsius temperature: "))

fahrenheit = (temperature * 9/5) + 32
kelvin = temperature + 273.15

print(f"Fahrenheit: {fahrenheit}")
print(f"Kelvin: {kelvin}")