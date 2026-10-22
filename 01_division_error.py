try:
    first = int(input("Enter first number: "))
    second = int(input("Enter second number: "))
    print("Result:", first / second)
except ZeroDivisionError:
    print("Cannot divide by zero.")
except ValueError:
    print("Please enter integers only.")
