
number=int(input("Enter a number:"))
if number < 0:
    print("enter a postive number")
else:
    total=0
    while(number > 0):
        num=number%10;
        total+=num
        number=number//10
    print("Sum of digit:",total)
