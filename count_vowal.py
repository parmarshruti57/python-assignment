st=input("Enter a string:").lower()
i=0
count_vowel=0
vowels="aeiou"
while(i < len(st)):
    if st[i] in vowels:
        count_vowel+=1
    i+=1

print("total number of vowels:",count_vowel)