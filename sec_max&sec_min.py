l1=[4,5,1,2,34,6,7,8,45,32,]
max_number=l1[0]
min_number=l1[0]
second_maxnumber=l1[0]
second_minnumber=l1[0]
for i in l1:
    if max_number < i:
        second_maxnumber=max_number
        max_number=i
    elif i > second_maxnumber and i != max_number:
        second_maxnumber=i
for i in l1:
    if min_number > i:
        second_minnumber=min_number
        min_number=i
    elif i < second_minnumber or i == min_number:
        second_minnumber=i
        
print(second_maxnumber)
print(second_minnumber)
