student=[]
def get_detail():
    name=input("Enter a name:")
    age=int(input("Enter a age:"))
    if age <=0:
        print("please enter a real age")
    course=input("Enter a course:")
    return {"name":name,"age":age,"course":course}

number=int(input("how many students details do want to  add:"))
if number <= 0:
    print("Enter a postive number")
else:
    for i in range(1,number+1):
        student_detail=get_detail()
        student.append(student_detail)
        
    print("==== Student Database ======")
    for i,detail in enumerate(student,start=1):
        print(f"Student   {i} ")
        print(f"Name:",detail['name'])
        print(f"Age:",detail['age'])
        print(f"Course:",detail['course'])
                                