
a=int(input("Enter a number 1:"))
b=int(input("Enter a number 2:"))
c=int(input("Enter a number 3:"))
if a>b and a>c:
    print(f"{a} is large")
elif b>a and b>c:
    print(f"{b} is large")
else:
    print(f"{c} is large")
