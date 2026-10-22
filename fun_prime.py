def is_prime(number):
    is_prime=True
    for i in range(2,number):
        if(number % i == 0):
            is_prime=False
            break
        
    if is_prime == True:
        return True
    else:
        return False
    
number=int(input("Enter  a number:"))
if is_prime(number) == True:
    print("this is prime number")
else:
    print("this is not prime number")
        
        