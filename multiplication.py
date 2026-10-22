
number =int(input("Enter a number:"))
if(number <= 0):
    print("Enter a postive number")
else:
    i=1
    while(i<=10):
        print(f"{number}*{i}={number*i}")
        i+=1