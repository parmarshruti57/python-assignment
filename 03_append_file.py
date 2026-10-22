with open("names.txt", "w") as file:
    file.write("Amit\nNeha\n")
name = input("Enter another name: ")
with open("names.txt", "a") as file:
    file.write(name + "\n")
with open("names.txt", "r") as file:
    print(file.read())
