with open("sentence.txt", "w") as file:
    file.write("Python is easy to learn")
with open("sentence.txt", "r") as file:
    text = file.read()
words = text.split()
print("Number of words:", len(words))
