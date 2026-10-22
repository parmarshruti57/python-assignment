def count_digit(text):
    total=0
    for ch in text:
        if ch in "1234567890":
            total+=1
    return total

text=input("Enter a text:")
print(count_digit(text))
    