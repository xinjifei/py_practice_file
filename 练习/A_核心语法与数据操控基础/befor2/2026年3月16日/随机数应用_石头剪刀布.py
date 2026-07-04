import random

random1=random.randint(1,3)
print(f' 电脑出了{random1}')

try:
    #电脑赢:
    random2=int(input('出招(石头=1，剪刀=2，布=3)'))
    if random1 == 1 and random2 == 2 or random1 == 2 and random2 == 3 or random1 == 3 and random2 == 1:
        print('--电脑赢--')

    #玩家赢：
    elif random1 == 1 and random2 == 3 or random1 == 2 and random2 == 1 or random1 == 3 and random2 == 2:
        print('--玩家赢--')

    elif random1 == random2:
        print('--平局--')

    else:
        print('--输入非法--')

    print(f'(玩家出招={random1},电脑出招={random2})')

except ValueError:
    print(f'输入的：‘{random2}’非法，请输入1到3之间的数字')