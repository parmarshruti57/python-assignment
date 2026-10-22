import CrudOp as c1


while True:

    print("\n==============================================")
    print("          EMPLOYEE MANAGEMENT SYSTEM")
    print("==============================================")
    print("1. Add Employee")
    print("2. Display All Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Sort Employees by Salary")
    print("7. Count Employees")
    print("8. Check Employee Age (22-30)")
    print("9. Check Salary Category")
    print("10. Exit")
    print("==============================================")

    choice = input("Enter your choice (1-10): ")
    print("----------------------------------------------")

    if choice == "1":
        c1.add()

    elif choice == "2":
        c1.display()

    elif choice == "3":
        c1.search()

    elif choice == "4":
        c1.update()

    elif choice == "5":
        c1.deletebyEID()

    elif choice == "6":
        c1.sortBySalary()

    elif choice == "7":
        c1.countEmployee()

    elif choice == "8":
        c1.checkAge()

    elif choice == "9":
        c1.salaryCategory()

    elif choice == "10":
        print("Thank You for using Employee Management System")
        break

    else:
        print("Invalid choice. Please enter between 1 and 10.")