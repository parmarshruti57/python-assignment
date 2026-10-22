
number=int(input("Enter a number:"))
if number < 0:
    print("please enter a postive number")
else:
    odd=0
    even=0
    temp=number
    
    while(number != 0):
        num=number%10
        if(num % 2 ==0):
            even+=1
        else:
            odd+=1
        number=number//10
    print("Number : ",temp)
    print("Total_odd:",odd)
    print("Total_even:",even)
