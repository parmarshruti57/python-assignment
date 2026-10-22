class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print("Name:", self.name)
        print("Salary:", self.salary)

employee1 = Employee("Amit", 20000)
employee2 = Employee("Priya", 25000)
employee1.display()
employee2.display()
