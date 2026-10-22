employee = []


def add():
    eid = int(input("Enter Employee ID: "))
    ename = input("Enter Employee Name: ")
    age = int(input("Enter Employee Age: "))
    department = input("Enter Department: ")
    salary = int(input("Enter Employee Salary: "))
    designation = input("Enter Designation: ")

    e1 = {
        "EID": eid,
        "EName": ename,
        "Age": age,
        "Department": department,
        "Salary": salary,
        "Designation": designation
    }

    employee.append(e1)

    print("Employee added successfully")


def display():
    if len(employee) == 0:
        print("No employee records available")
    else:
        print("================================================================")
        print("ID\tName\t\tAge\tDepartment\tSalary\tDesignation")
        print("================================================================")

        for e1 in employee:
            print(e1["EID"], "\t", e1["EName"], "\t\t",
                  e1["Age"], "\t", e1["Department"], "\t\t",
                  e1["Salary"], "\t", e1["Designation"])


def search():
    eid = int(input("Enter Employee ID to search: "))
    found = 0

    for e1 in employee:
        if e1["EID"] == eid:
            found = 1
            break

    if found == 1:
        print("Employee is found")
        print("----------------------------------")
        print("Employee ID :", e1["EID"])
        print("Name        :", e1["EName"])
        print("Age         :", e1["Age"])
        print("Department  :", e1["Department"])
        print("Salary      :", e1["Salary"])
        print("Designation :", e1["Designation"])
    else:
        print("Employee not found")


def update():
    eid = int(input("Enter Employee ID to update: "))
    found = 0

    for e1 in employee:
        if e1["EID"] == eid:
            found = 1
            break

    if found == 1:
        print("Employee is found")
        print("1. Update Name")
        print("2. Update Age")
        print("3. Update Department")
        print("4. Update Salary")
        print("5. Update Designation")

        choice = input("Enter your choice: ")

        if choice == "1":
            e1["EName"] = input("Enter New Name: ")
            print("Name updated successfully")

        elif choice == "2":
            e1["Age"] = int(input("Enter New Age: "))
            print("Age updated successfully")

        elif choice == "3":
            e1["Department"] = input("Enter New Department: ")
            print("Department updated successfully")

        elif choice == "4":
            e1["Salary"] = int(input("Enter New Salary: "))
            print("Salary updated successfully")

        elif choice == "5":
            e1["Designation"] = input("Enter New Designation: ")
            print("Designation updated successfully")

        else:
            print("Invalid choice")

    else:
        print("Employee not found")


def deletebyEID():
    eid = int(input("Enter Employee ID to delete: "))
    found = 0

    for e1 in employee:
        if e1["EID"] == eid:
            employee.remove(e1)
            found = 1
            print("Employee deleted successfully")
            break

    if found == 0:
        print("Employee not found")


def sortBySalary():
    if len(employee) == 0:
        print("No employee records available")
    else:
        employee.sort(key=lambda x: x["Salary"])
        print("Employees sorted by salary")
        display()


def countEmployee():
    print("Total number of employees:", len(employee))


def checkAge():
    if len(employee) == 0:
        print("No employee records available")
        return

    found = 0

    print("----------------------------------")
    print("Employees between age 22 and 30")
    print("----------------------------------")

    for e1 in employee:
        if e1["Age"] >= 22 and e1["Age"] <= 30:
            print("Employee ID :", e1["EID"])
            print("Name        :", e1["EName"])
            print("Age         :", e1["Age"])
            print("Department  :", e1["Department"])
            print("----------------------------------")
            found = 1

    if found == 0:
        print("No employee between age 22 and 30")


def salaryCategory():
    eid = int(input("Enter Employee ID: "))
    found = 0

    for e1 in employee:
        if e1["EID"] == eid:
            found = 1
            break

    if found == 1:
        print("Employee Name :", e1["EName"])
        print("Salary        :", e1["Salary"])

        if e1["Salary"] < 20000:
            print("Salary Category : Low Salary")

        elif e1["Salary"] <= 50000:
            print("Salary Category : Medium Salary")

        else:
            print("Salary Category : High Salary")

    else:
        print("Employee not found")