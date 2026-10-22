l1=[6,3,2,6,7,8,92,]
i=0
while(i<len(l1)):
    j=i+1
    while(j < len(l1)):
        if l1[j] == l1[i]:
           l1.pop(j) 
        else:
            j+=1        
        j+=1
    i+=1
print(l1)
 