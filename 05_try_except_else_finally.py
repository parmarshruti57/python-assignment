try:
    number = int(input("Enter an integer: "))
except ValueError:
    print("Invalid input.")
else:
    print("Square:", number * number)
finally:
    print("Program finished.")
