with open("student.txt", "w") as file:
    file.write("Name: Rahul\nCourse: BCA\n")
with open("student.txt", "r") as file:
    print(file.read())
