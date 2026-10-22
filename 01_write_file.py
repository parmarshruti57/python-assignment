text = input("Enter a message: ")
with open("message.txt", "w") as file:
    file.write(text)
print("Message saved.")
