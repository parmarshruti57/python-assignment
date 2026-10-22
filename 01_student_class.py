class Student:
    def display(self):
        print("Name:", self.name)
        print("Roll number:", self.roll_number)

student = Student()
student.name = "Rahul"
student.roll_number = 101
student.display()
