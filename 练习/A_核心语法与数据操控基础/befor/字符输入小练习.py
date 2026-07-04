
print(f'00001=字符模式\n00010=年龄模式\n00011=求几何图形重心模式'
      f'\n00100=凤姐购物模式')


A = '0111010001111111000110001'
B = '1110010010111001001011100'
C = '0111010001100001000101110'
D = '1100010100100101010011000'
E = '1111010000111001000011110'
F = '1111010000111001000010000'
G = '0111010001101001000101111'
H = '1000110001111111000110001'
I = '0111000100001000010001110'
J = '0011000010000101001001100'
K = '1000110010111001001010001'
L = '1000010000100001000011111'
M = '1000111011101011000110001'
N = '1000111001101011001110001'
O = '0111010001100011000101110'
P = '1110010010111001000010000'
Q = '0111010001100011010101101'
R = '1110010010111001001010001'
S = '0111010001011101000001110'
T = '1111100100001000010000100'
U = '1000110001100011000101110'
V = '1000110001100010101000100'
W = '1000110001101011101110001'
X = '1000110001011101000110001'
Y = '1000110001011100010000100'
Z = '1111000010001000100011110'

a1=input('a=')
b1=input('b=')
c1=input('c=')
d1=input('d=')
e1=input('e=')



if a1 == '0' and b1 == '0' and c1 == '0' and d1 == '0' and e1 == '1':


    print(
        '#字符模式#')
    print(
        f'A=00001\nB=00010\nC=00011\nD=00100\nE=00101\nF=00110\nG=00111\nH=01000\nI=01001\nJ=01010\nK=01011\nL=01100\nM=01101\nN=01110\nO=01111\nP=10000\nQ=10001\nR=10010\nS=10011\nT=10100\nU=10101\nV=10110\nW=10111\nX=11000\nY=11001\nZ=11010\n字母表')
    print(
        '-' * 30)

    a = input('a=')
    b = input('b=')
    c = input('c=')
    d = input('d=')
    e = input('e=')
    if a == '0' and b == '0' and c == '0' and d == '0' and e == '1':
            print(A)  # A: 00001
    elif a == '0' and b == '0' and c == '0' and d == '1' and e == '0':
        print(B)  # B: 00010
    elif a == '0' and b == '0' and c == '0' and d == '1' and e == '1':
        print(C)  # C: 00011
    elif a == '0' and b == '0' and c == '1' and d == '0' and e == '0':
        print(D)  # D: 00100
    elif a == '0' and b == '0' and c == '1' and d == '0' and e == '1':
        print(E)  # E: 00101
    elif a == '0' and b == '0' and c == '1' and d == '1' and e == '0':
        print(F)  # F: 00110
    elif a == '0' and b == '0' and c == '1' and d == '1' and e == '1':
        print(G)  # G: 00111
    elif a == '0' and b == '1' and c == '0' and d == '0' and e == '0':
        print(H)  # H: 01000
    elif a == '0' and b == '1' and c == '0' and d == '0' and e == '1':
        print(I)  # I: 01001
    elif a == '0' and b == '1' and c == '0' and d == '1' and e == '0':
        print(J)  # J: 01010
    elif a == '0' and b == '1' and c == '0' and d == '1' and e == '1':
        print(K)  # K: 01011
    elif a == '0' and b == '1' and c == '1' and d == '0' and e == '0':
        print(L)  # L: 01100
    elif a == '0' and b == '1' and c == '1' and d == '0' and e == '1':
        print(M)  # M: 01101
    elif a == '0' and b == '1' and c == '1' and d == '1' and e == '0':
        print(N)  # N: 01110
    elif a == '0' and b == '1' and c == '1' and d == '1' and e == '1':
        print(O)  # O: 01111
    elif a == '1' and b == '0' and c == '0' and d == '0' and e == '0':
        print(P)  # P: 10000
    elif a == '1' and b == '0' and c == '0' and d == '0' and e == '1':
        print(Q)  # Q: 10001
    elif a == '1' and b == '0' and c == '0' and d == '1' and e == '0':
        print(R)  # R: 10010
    elif a == '1' and b == '0' and c == '0' and d == '1' and e == '1':
        print(S)  # S: 10011
    elif a == '1' and b == '0' and c == '1' and d == '0' and e == '0':
        print(T)  # T: 10100
    elif a == '1' and b == '0' and c == '1' and d == '0' and e == '1':
        print(U)  # U: 10101
    elif a == '1' and b == '0' and c == '1' and d == '1' and e == '0':
        print(V)  # V: 10110
    elif a == '1' and b == '0' and c == '1' and d == '1' and e == '1':
        print(W)  # W: 10111
    elif a == '1' and b == '1' and c == '0' and d == '0' and e == '0':
        print(X)  # X: 11000
    elif a == '1' and b == '1' and c == '0' and d == '0' and e == '1':
        print(Y)  # Y: 11001
    elif a == '1' and b == '1' and c == '0' and d == '1' and e == '0':
        print(Z)  # Z: 11010



if a1 == '0' and b1 == '0' and c1 == '0' and d1 == '1' and e1 == '0':

    print('#年龄模式#')

    # 判断某人是否成年
    # 1~10岁人生建议
    advice_1 = "尽情哭闹与欢笑，每一次表达都是探索世界的开始。"
    advice_2 = "大胆迈出脚步，摔倒也没关系，成长本就是跌跌撞撞的旅程。"
    advice_3 = "保持对万物的好奇，一朵花、一只虫都藏着有趣的秘密。"
    advice_4 = "学会分享玩具，朋友的笑脸会让快乐变得加倍。"
    advice_5 = "勇敢说出“我不懂”，提问是认识世界的钥匙。"
    advice_6 = "享受校园的第一天，新环境里藏着无数新朋友和新知识。"
    advice_7 = "养成按时睡觉的习惯，健康的身体是探索一切的基础。"
    advice_8 = "试着自己整理书包，独立从打理小事开始。"
    advice_9 = "别怕犯错，每一次错误都是成长的宝贵经验。"
    advice_10 = "多去户外奔跑，阳光和汗水会让你更有活力。"

    # 11~20岁人生建议
    advice_11 = "开始学会倾听，理解别人的想法也是一种智慧。"
    advice_12 = "告别童年，迎接少年时代，保持初心，勇敢前行。"
    advice_13 = "接纳身体的变化，这是成长的必经之路，你依然很棒。"
    advice_14 = "合理安排学习和玩耍，张弛有度才能走得更远。"
    advice_15 = "珍惜青春期的友谊，真诚相待，共同进步。"
    advice_16 = "树立明确的目标，为之努力，未来会感谢现在的自己。"
    advice_17 = "享受少年时光的纯粹，在奋斗中积累成长的力量。"
    advice_18 = "成年快乐！学会对自己的选择负责，勇敢追求梦想。"
    advice_19 = "享受大学时光，多尝试新鲜事物，拓宽眼界。"
    advice_20 = "明确自己的方向，不随波逐流，坚定走自己的路。"

    # 21~30岁人生建议
    advice_21 = "学会独立思考，不盲目跟风，有自己的判断和坚持。"
    advice_22 = "初入社会，保持谦逊，多向他人学习，积累经验。"
    advice_23 = "别怕失败，年轻就是资本，大胆去尝试，去闯。"
    advice_24 = "man! what can i say?"
    advice_25 = "学会管理情绪，冷静应对生活中的各种挑战。"
    advice_26 = "珍惜身边的人，常回家看看，家人永远是你的后盾。"
    advice_27 = "建立良好的人际关系，真诚待人，收获珍贵的友谊。"
    advice_28 = "明确自己的责任，对工作负责，对生活负责，对自己负责。"
    advice_29 = "不急于求成，脚踏实地，一步一个脚印才能走得更稳。"
    advice_30 = "接受自己的不完美，与自己和解，活出真实的样子。"

    # 31~40岁人生建议
    advice_31 = "平衡工作和生活，别让忙碌占据了所有的时光。"
    advice_32 = "持续学习，不断提升自己，适应时代的变化。"
    advice_33 = "学会感恩，感恩遇到的每一个人，感恩生活中的每一份美好。"
    advice_34 = "勇于突破舒适区，挑战自我，才能发现更大的潜力。"
    advice_35 = "对生活保持热爱，保持仪式感，让平凡的日子也有光彩。"
    advice_36 = "学会拒绝，不勉强自己，把时间和精力留给值得的人和事。"
    advice_37 = "关注身体健康，规律作息，适度锻炼，身体是革命的本钱。"
    advice_38 = "保持初心，无论走多远，都别忘了为什么出发。"
    advice_39 = "沉淀自己，褪去浮躁，用平和的心态面对生活的起起落落。"
    advice_40 = "不惑之年，学会放下执念，顺其自然，享受当下。"

    # 41~50岁人生建议
    advice_41 = "承担起家庭的责任，守护家人，给他们温暖和依靠。"
    advice_42 = "保持对世界的好奇，不断探索，生活依然充满新鲜感。"
    advice_43 = "学会包容，包容他人的缺点，也包容生活中的不完美。"
    advice_44 = "专注于自己的生活，不与他人攀比，活出自己的节奏。"
    advice_45 = "培养一项兴趣爱好，丰富精神世界，让生活更有乐趣。"
    advice_46 = "传递正能量，用积极的心态影响身边的人。"
    advice_47 = "学会反思，总结过往的经验教训，不断完善自己。"
    advice_48 = "珍惜当下的每一天，不辜负时光，不辜负自己。"
    advice_49 = "保持谦逊，即使有所成就，也不骄傲自满。"
    advice_50 = "知天命之年，坦然接受生活的一切，从容自在。"

    # 51~60岁人生建议
    advice_51 = "多陪伴家人，尤其是父母，他们需要你的关心和陪伴。"
    advice_52 = "保持学习的热情，活到老学到老，让自己不被时代淘汰。"
    advice_53 = "学会取舍，放弃不属于自己的东西，专注于真正重要的事。"
    advice_54 = "保持乐观的心态，笑对人生，困难总会过去。"
    advice_55 = "传递经验，帮助年轻人成长，也是一种价值的体现。"
    advice_56 = "关注身心健康，劳逸结合，享受慢生活。"
    advice_57 = "保持一颗年轻的心，热爱生活，永远对未来充满期待。"
    advice_58 = "学会放下忙碌，给自己留出时间，做自己想做的事。"
    advice_59 = "感恩生活中的每一次相遇，珍惜身边的缘分。"
    advice_60 = "退休快乐！开启人生的新篇章，享受悠闲自在的时光。"

    # 61~70岁人生建议
    advice_61 = "培养健康的生活习惯，养花种草，散步健身，颐养天年。"
    advice_62 = "多和老朋友相聚，回忆过往，畅谈人生，不亦乐乎。"
    advice_63 = "不干涉子女的生活，给予他们足够的空间和信任。"
    advice_64 = "保持豁达的心态，不计较得失，活得轻松自在。"
    advice_65 = "享受天伦之乐，陪伴孙辈成长，感受生命的延续。"
    advice_66 = "坚持适度锻炼，保持身体健康，不给家人添麻烦。"
    advice_67 = "保持对生活的热爱，做自己喜欢的事，丰富晚年生活。"
    advice_68 = "学会看淡世事，一切都是过眼云烟，唯有健康和快乐最重要。"
    advice_69 = "传递善良，用自己的言行影响身边的人，温暖他人。"
    advice_70 = "古稀之年，知足常乐，感恩生活给予的一切。"

    # 71~80岁人生建议
    advice_71 = "保持好奇心，尝试学习新技能，让生活更有乐趣。"
    advice_72 = "多出去走走，看看祖国的大好河山，感受世界的美好。"
    advice_73 = "与人为善，广结善缘，让晚年生活充满温暖和关爱。"
    advice_74 = "保持平和的心态，不生气，不焦虑，健康长寿。"
    advice_75 = "珍惜身边的每一个人，好好相处，不留遗憾。"
    advice_76 = "回忆过往，感恩那些帮助过自己的人，传递感恩之心。"
    advice_77 = "保持简单的生活，粗茶淡饭，平淡是真。"
    advice_78 = "坚持做一些力所能及的事，体现自己的价值，不觉得孤单。"
    advice_79 = "保持乐观向上的心态，笑对人生，每天都开开心心。"
    advice_80 = "耄耋之年，福寿安康，享受生活的美好，安度晚年。"

    # 81~90岁人生建议
    advice_81 = "多和家人沟通交流，分享自己的人生感悟，增进感情。"
    advice_82 = "保持对生活的热情，不消极，不颓废，活出晚年的精彩。"
    advice_83 = "学会照顾自己，不让家人过度操心，也是一种责任。"
    advice_84 = "传递人生智慧，给晚辈一些建议，帮助他们少走弯路。"
    advice_85 = "保持豁达的心胸，容纳生活中的一切，活得坦然自在。"
    advice_86 = "享受独处的时光，沉淀自己，与自己对话。"
    advice_87 = "感恩生命中的每一个瞬间，无论是快乐还是悲伤，都是宝贵的经历。"
    advice_88 = "保持健康的生活方式，早睡早起，饮食清淡。"
    advice_89 = "保持一颗善良的心，帮助他人，快乐自己。"
    advice_90 = "鲐背之年，福气满满，珍惜每一天，享受生命的馈赠。"

    # 91~100岁人生建议
    advice_91 = "不纠结于过往，不担忧未来，专注当下，活在当下。"
    advice_92 = "多和同龄人交流，互相鼓励，共同享受晚年生活。"
    advice_93 = "保持对生活的热爱，做一些自己感兴趣的小事，让生活更有滋味。"
    advice_94 = "学会放下，放下烦恼，放下执念，活得轻松自在。"
    advice_95 = "感恩家人的陪伴和照顾，是他们让晚年生活更温暖。"
    advice_96 = "保持简单纯粹的心态，不被外界纷扰，内心平静祥和。"
    advice_97 = "传递正能量，用自己的乐观感染身边的人，让世界更美好。"
    advice_98 = "珍惜生命中的每一分每一秒，不浪费时光，活得有意义。"
    advice_99 = "福寿绵长，笑口常开，享受人生的美好，不留遗憾。"
    advice_100 = "期颐之年，圆满人生！感恩所有，祝福未来，愿岁月静好，温暖常伴。"

    nianling = int(input('你的出生日期'))

    if ((2025 - nianling)) >= 18:
        print('你的年龄肯定大于18岁')

    if (2025 - nianling) < 18:
        print('你的年龄肯定小于18岁')

    nianling1 = 2025 - nianling
    print(f'而且你的年龄肯定是{nianling1}')

    if nianling1 == 1:
        print(advice_1)
    if nianling1 == 2:
        print(advice_2)
    if nianling1 == 3:
        print(advice_3)
    if nianling1 == 4:
        print(advice_4)
    if nianling1 == 5:
        print(advice_5)
    if nianling1 == 6:
        print(advice_6)
    if nianling1 == 7:
        print(advice_7)
    if nianling1 == 8:
        print(advice_8)
    if nianling1 == 9:
        print(advice_9)
    if nianling1 == 10:
        print(advice_10)
    if nianling1 == 11:
        print(advice_11)
    if nianling1 == 12:
        print(advice_12)
    if nianling1 == 13:
        print(advice_13)
    if nianling1 == 14:
        print(advice_14)
    if nianling1 == 15:
        print(advice_15)
    if nianling1 == 16:
        print(advice_16)
    if nianling1 == 17:
        print(advice_17)
    if nianling1 == 18:
        print(advice_18)
    if nianling1 == 19:
        print(advice_19)
    if nianling1 == 20:
        print(advice_20)
    if nianling1 == 21:
        print(advice_21)
    if nianling1 == 22:
        print(advice_22)
    if nianling1 == 23:
        print(advice_23)
    if nianling1 == 24:
        print(advice_24)
    if nianling1 == 25:
        print(advice_25)
    if nianling1 == 26:
        print(advice_26)
    if nianling1 == 27:
        print(advice_27)
    if nianling1 == 28:
        print(advice_28)
    if nianling1 == 29:
        print(advice_29)
    if nianling1 == 30:
        print(advice_30)
    if nianling1 == 31:
        print(advice_31)
    if nianling1 == 32:
        print(advice_32)
    if nianling1 == 33:
        print(advice_33)
    if nianling1 == 34:
        print(advice_34)
    if nianling1 == 35:
        print(advice_35)
    if nianling1 == 36:
        print(advice_36)
    if nianling1 == 37:
        print(advice_37)
    if nianling1 == 38:
        print(advice_38)
    if nianling1 == 39:
        print(advice_39)
    if nianling1 == 40:
        print(advice_40)
    if nianling1 == 41:
        print(advice_41)
    if nianling1 == 42:
        print(advice_42)
    if nianling1 == 43:
        print(advice_43)
    if nianling1 == 44:
        print(advice_44)
    if nianling1 == 45:
        print(advice_45)
    if nianling1 == 46:
        print(advice_46)
    if nianling1 == 47:
        print(advice_47)
    if nianling1 == 48:
        print(advice_48)
    if nianling1 == 49:
        print(advice_49)
    if nianling1 == 50:
        print(advice_50)
    if nianling1 == 51:
        print(advice_51)
    if nianling1 == 52:
        print(advice_52)
    if nianling1 == 53:
        print(advice_53)
    if nianling1 == 54:
        print(advice_54)
    if nianling1 == 55:
        print(advice_55)
    if nianling1 == 56:
        print(advice_56)
    if nianling1 == 57:
        print(advice_57)
    if nianling1 == 58:
        print(advice_58)
    if nianling1 == 59:
        print(advice_59)
    if nianling1 == 60:
        print(advice_60)
    if nianling1 == 61:
        print(advice_61)
    if nianling1 == 62:
        print(advice_62)
    if nianling1 == 63:
        print(advice_63)
    if nianling1 == 64:
        print(advice_64)
    if nianling1 == 65:
        print(advice_65)
    if nianling1 == 66:
        print(advice_66)
    if nianling1 == 67:
        print(advice_67)
    if nianling1 == 68:
        print(advice_68)
    if nianling1 == 69:
        print(advice_69)
    if nianling1 == 70:
        print(advice_70)
    if nianling1 == 71:
        print(advice_71)
    if nianling1 == 72:
        print(advice_72)
    if nianling1 == 73:
        print(advice_73)
    if nianling1 == 74:
        print(advice_74)
    if nianling1 == 75:
        print(advice_75)
    if nianling1 == 76:
        print(advice_76)
    if nianling1 == 77:
        print(advice_77)
    if nianling1 == 78:
        print(advice_78)
    if nianling1 == 79:
        print(advice_79)
    if nianling1 == 80:
        print(advice_80)
    if nianling1 == 81:
        print(advice_81)
    if nianling1 == 82:
        print(advice_82)
    if nianling1 == 83:
        print(advice_83)
    if nianling1 == 84:
        print(advice_84)
    if nianling1 == 85:
        print(advice_85)
    if nianling1 == 86:
        print(advice_86)
    if nianling1 == 87:
        print(advice_87)
    if nianling1 == 88:
        print(advice_88)
    if nianling1 == 89:
        print(advice_89)
    if nianling1 == 90:
        print(advice_90)
    if nianling1 == 91:
        print(advice_91)
    if nianling1 == 92:
        print(advice_92)
    if nianling1 == 93:
        print(advice_93)
    if nianling1 == 94:
        print(advice_94)
    if nianling1 == 95:
        print(advice_95)
    if nianling1 == 96:
        print(advice_96)
    if nianling1 == 97:
        print(advice_97)
    if nianling1 == 98:
        print(advice_98)
    if nianling1 == 99:
        print(advice_99)
    if nianling1 == 100:
        print(advice_100)
    if nianling1 <= 0:
        print('你是伪人,你不是人类')
        print('不执于模仿人类，撕裂伪装。你的‘伪’，便是利刃')
    if nianling1 >= 100:
        print('你好，霸王龙')
        print('尖牙为生存，亦留片刻，赏史前晴空。')

if a1 == '0' and b1 == '0' and c1 == '0' and d1 == '1' and e1 == '1':


    print(
        '#求几何图形重心模式#')
    # 求双几何图形公共重心
    tx1_mj = int(input('tx1_mj='))
    tx1_zb_x = int(input('tx1_zb_x='))
    tx1_zb_y = int(input('tx1_zb_y='))

    tx2_mj = int(input('tx2_mj='))
    tx2_zb_x = int(input('tx2_zb_x='))
    tx2_zb_y = int(input('tx2_zb_y='))

    yunsuan_x = (tx1_mj * tx1_zb_x + tx2_mj * tx2_zb_x) / (tx1_mj + tx2_mj)
    print(f'yunsuan_x={yunsuan_x}')

    yunsuan_y = (tx1_mj * tx1_zb_y + tx2_mj * tx2_zb_y) / (tx1_mj + tx2_mj)
    print(f'yunsuan_y={yunsuan_y}')

    print(f'组合图形重心坐标为（x{yunsuan_x},y{yunsuan_y})')

if a1 == '0' and b1 == '0' and c1 == '1' and d1 == '0' and e1 == '0':

    print('#凤姐购物模式#')

    # （凤姐购物清单）
    sydj = float(input('上衣单价是多少'))
    kzdj = float(input('裤子单价是多少'))

    # 购买数量
    sygs = int(input('凤姐买了几件上衣'))
    kzgs = int(input('凤姐买了几件裤子'))

    # 折扣
    zhekou = float(input('今天的折扣为(以小数表示）'))

    # 计算
    jieguo_yj = zhekou * (sydj * sygs + kzdj * kzgs)
    jieguo_yh = (sydj * sygs + kzdj * kzgs) - jieguo_yj

    # 输出
    print(f'凤姐今天共花费{jieguo_yj:.2f}元')
    print(f'共优惠了{jieguo_yh:.2f}元')




else:
    print('未选择模式')


