filename = input("Enter a file name: ")
try:
    with open(filename, "r") as file:
        print(file.read())
except FileNotFoundError:
    print("File does not exist.")
