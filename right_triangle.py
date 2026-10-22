
number=int(input("Enter a number:"))
if number < 0:
    print("Enter a postive number")
else:
    for i in range(1,number+1):
        for j in range(1,i+1):
            print("*",end=" ")
        print(" ")


