numbers=[22,43,56,42,34]

max_number=numbers[0]
for num in numbers:
    if num > max_number:
        max_number=num
    
print("Maximum number:",max_number)
min_number=numbers[0]
for num in numbers:
    if num < min_number:
        min_number=num

print("Minimum number:",min_number)