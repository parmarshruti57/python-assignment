for i in range(1,6):
    for  _ in range(5-i):
        print(" ",end=" ")
    for j in range(5,5-i,-1):
        print(j,end=" ")
    print()