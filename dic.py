student={}
name=input("Enter a name:")
age=int(input("Enter a age:"))
course=input("Enter a course:")
student.update({"name":name,"age":age,"Course":course})
print("===== Student Details ======")
for key_detail,value_details in student.items():
    print(f"{key_detail}   : {value_details}")
    