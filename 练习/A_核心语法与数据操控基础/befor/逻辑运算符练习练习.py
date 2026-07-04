
#输入端口
a=input('1=')
b=input('2=')
c=input('3=')
d=input('4=')
e=input('5=')

# 字母a-z 依次对应5位二进制 00001~01100（共26个，覆盖a-z）
a00001 = a == 0 and b == 0 and c == 0 and d == 0 and e == 1  # 00001 → 十进制1
b00010 = a == 0 and b == 0 and c == 0 and d == 1 and e == 0  # 00010 → 十进制2
c00011 = a == 0 and b == 0 and c == 0 and d == 1 and e == 1  # 00011 → 十进制3
d00100 = a == 0 and b == 0 and c == 1 and d == 0 and e == 0  # 00100 → 十进制4
e00101 = a == 0 and b == 0 and c == 1 and d == 0 and e == 1  # 00101 → 十进制5
f00110 = a == 0 and b == 0 and c == 1 and d == 1 and e == 0  # 00110 → 十进制6
g00111 = a == 0 and b == 0 and c == 1 and d == 1 and e == 1  # 00111 → 十进制7
h01000 = a == 0 and b == 1 and c == 0 and d == 0 and e == 0  # 01000 → 十进制8
i01001 = a == 0 and b == 1 and c == 0 and d == 0 and e == 1  # 01001 → 十进制9
j01010 = a == 0 and b == 1 and c == 0 and d == 1 and e == 0  # 01010 → 十进制10
k01011 = a == 0 and b == 1 and c == 0 and d == 1 and e == 1  # 01011 → 十进制11
l01100 = a == 0 and b == 1 and c == 1 and d == 0 and e == 0  # 01100 → 十进制12
m01101 = a == 0 and b == 1 and c == 1 and d == 0 and e == 1  # 01101 → 十进制13
n01110 = a == 0 and b == 1 and c == 1 and d == 1 and e == 0  # 01110 → 十进制14
o01111 = a == 0 and b == 1 and c == 1 and d == 1 and e == 1  # 01111 → 十进制15
p10000 = a == 1 and b == 0 and c == 0 and d == 0 and e == 0  # 10000 → 十进制16
q10001 = a == 1 and b == 0 and c == 0 and d == 0 and e == 1  # 10001 → 十进制17
r10010 = a == 1 and b == 0 and c == 0 and d == 1 and e == 0  # 10010 → 十进制18
s10011 = a == 1 and b == 0 and c == 0 and d == 1 and e == 1  # 10011 → 十进制19
t10100 = a == 1 and b == 0 and c == 1 and d == 0 and e == 0  # 10100 → 十进制20
u10101 = a == 1 and b == 0 and c == 1 and d == 0 and e == 1  # 10101 → 十进制21
v10110 = a == 1 and b == 0 and c == 1 and d == 1 and e == 0  # 10110 → 十进制22
w10111 = a == 1 and b == 0 and c == 1 and d == 1 and e == 1  # 10111 → 十进制23
x11000 = a == 1 and b == 1 and c == 0 and d == 0 and e == 0  # 11000 → 十进制24
y11001 = a == 1 and b == 1 and c == 0 and d == 0 and e == 1  # 11001 → 十进制25
z11010 = a == 1 and b == 1 and c == 0 and d == 1 and e == 0  # 11010 → 十进制26





