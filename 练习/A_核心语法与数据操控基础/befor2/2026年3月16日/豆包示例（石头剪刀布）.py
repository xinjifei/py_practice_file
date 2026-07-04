import random

# 电脑出招
random1 = random.randint(1, 3)
# 提前定义输入字符串，避免IDE警告
input_str = ""


# 第一步：先存用户输入的原始内容（不管输啥都能存）
input_str = input('出招(石头=1，剪刀=2，布=3)：')
# 第二步：再尝试转成数字
random2 = int(input_str)

# 电脑赢的条件
if (random1 == 1 and random2 == 2) or (random1 == 2 and random2 == 3) or (random1 == 3 and random2 == 1):
    print('--电脑赢--')
# 玩家赢的条件
elif (random1 == 1 and random2 == 3) or (random1 == 2 and random2 == 1) or (random1 == 3 and random2 == 2):
    print('--玩家赢--')
# 平局
elif random1 == random2:
    print('--平局--')
# 输入数字但不在1-3范围
else:
    print('--输入非法--')

    # 修正：玩家和电脑出招显示顺序（之前写反了）
    print(f'(玩家出招={random2}, 电脑出招={random1})')