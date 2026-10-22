numbers = [10, 20, 30, 40, 50]
try:
    index = int(input("Enter an index from 0 to 4: "))
    print("Value:", numbers[index])
except IndexError:
    print("Index is out of range.")
except ValueError:
    print("Please enter an integer.")
