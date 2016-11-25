def test():
    all_student = {1: "John", 2: "Jane"}
    print (all_student)
    print (all_student[1])


class Student:
    def __init__(self, n, a):
        self.name = n
        self.age = a

    def say_hi(self):
        print ("My name is {} and I am {} years old".format(self.name, self.age))

def register_students():
    all_students = {}
    student1 = Student("Zubair", 18)
    student2 = Student("Ken", 18)
    student1.say_hi()

    say_hi(student1)

    all_students = { 1: student1, 2: student2 }


register_students()
