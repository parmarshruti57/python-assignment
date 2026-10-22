n=int(input("Enter a number:"))
temp=n
rev=0
while(n!=0):
    re=n%10
    rev=rev*10+re
    n=n//10
if(temp == rev):
    print("This is palidrome")
else:
    print("this is not palidrom")
print(rev)