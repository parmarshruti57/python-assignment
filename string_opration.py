st = input("Enter a string: ")
print("1.find length\n2.string in uppercase\n3.string in lowercase\n4.string with initial capital\n5.split the string\n6.Exit")

while True:
    choice = int(input("Enter a choice: "))
    match choice:
        case 1:
            print(len(st))
            
        case 2:
            print(st.upper())

        case 3:
            print(st.lower())
            
        case 4:
            print(st.capitalize())
            
        case 5:
            print(st.split())
            
        case 6:
            exit()
            break
