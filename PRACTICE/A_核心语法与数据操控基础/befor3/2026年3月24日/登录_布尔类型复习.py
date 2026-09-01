'''#练习一：判断是否成年
age = int(input("enter your age"))

is_adult = age >= 18

print(is_adult)
'''

'''
#练习二：用户登录
user_id = input("enter your user id")
password = input("enter your password")


is_id_correct = user_id == "lchh314"
is_password_correct = password == "123456"

if is_id_correct == True and is_password_correct == True:
    print("you are logged in")

else:
    print("wrong password or wrong username")
'''

#练习三：用户登录（加次数限制）

user_id = input("enter your user id")
password = input("enter your password")
user_correct = user_id == "lchh314" and password == "123456"

increment_count = 0
remaining_reps = 3

if user_correct == True:
    print("you are logged in")

else:
    while user_correct == False:
        remaining_reps -= 1

        print(f"wrong password or wrong username,remaining reps={remaining_reps}")
        if remaining_reps == 0:
            print('Your account is locked')
            break

        user_id = input("enter your user id")
        password = input("enter your password")
        user_correct = user_id == "lchh314" and password == "123456"

        if user_correct == True:
            print("you are logged in")

        increment_count += 1


