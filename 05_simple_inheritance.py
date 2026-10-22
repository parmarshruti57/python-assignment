class Person:
    def __init__(self, name):
        self.name = name

    def show_name(self):
        print("Name:", self.name)

class Student(Person):
    def show_course(self):
        print("Course: BCA")

student = Student("Riya")
student.show_name()
student.show_course()
