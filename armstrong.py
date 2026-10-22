n=int(input("Enter a number:"))
temp=n
rev=0
while(n!=0):
    re=n%10
    rev=re**3+rev
    n=n//10
if(temp == rev):
    print("This is armstrong")
else:
    print("this is not armstrong")
print(rev)