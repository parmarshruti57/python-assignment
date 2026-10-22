l1=[4,2,7,6,8,3,9,1]
i=0
while(i < len(l1)):
    j=i+1
    while(j < len(l1)):
        if l1[j] < l1[i]:
            temp=l1[j]
            l1[j]=l1[i]
            l1[i]=temp
        j+=1
    i+=1
            
print("Acending order:-",l1)
i=0
while(i < len(l1)):
    j=i+1
    while(j < len(l1)):
        if l1[j] > l1[i]:
            temp=l1[j]
            l1[j]=l1[i]
            l1[i]=temp
        j+=1
    i+=1
print("Decending order:-",l1)