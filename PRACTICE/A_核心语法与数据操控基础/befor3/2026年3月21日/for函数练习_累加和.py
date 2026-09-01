a = 0
b = 0

for a in range(0,100,1):
    if a > 100:
        break
    b += a
    a += 1

print(b)