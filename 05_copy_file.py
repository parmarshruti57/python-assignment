with open("source.txt", "w") as file:
    file.write("Welcome to Python practical.")
with open("source.txt", "r") as file:
    text = file.read()
with open("copy.txt", "w") as file:
    file.write(text)
print("File copied successfully.")
