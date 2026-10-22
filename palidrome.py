try:
    number=int(input("Enter number:"))
    if number <= 0:
        print("Enter a postive number")
    else:
        rev=0
        temp=number
        while(number != 0):
            re=number%10
            rev=rev*10+re
            number=number//10
        if temp == rev:
            print("This is number palidrome")
        else:
            print("this is not palidrome")
except ValueError:
    print("enter a number")