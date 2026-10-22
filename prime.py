n=int(input("Enter a number:"))
if(n<=1):
    print("This is not prime number")
else:
    is_prime=True
    for i in range(2,n):
        if(n%i==0):
            is_prime=False
            break

if is_prime==True:
    print("This is prime number")
else:
    print("This is not prime number")
    