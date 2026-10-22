
number =int(input("Enter a number:"))
if number <=0:
    print("please enter a postive number")
else:
    fact=1
    i=1
    for i in range(i,number+i):
        fact=fact*i
        i+=1
    print("Factrioal:",fact)
