
number=int(input("Enter a number:"))
if number < 0:
    print("Enter a postive number")
else:
    for i in range(number , 0,-1):
        for j in range(i,0,-1):
            print("*",end=" ")
        print(" ")
