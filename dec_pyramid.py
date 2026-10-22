
number=int(input("Enter a number:"))
if number < 0:
    print("Enter a postive number")
else:
    for i in range(number,0,-1):
        for _ in range(number-i):
            print("  ",end="")
        for j in range(1,i*2):
            print("*",end=" ")
        print()

