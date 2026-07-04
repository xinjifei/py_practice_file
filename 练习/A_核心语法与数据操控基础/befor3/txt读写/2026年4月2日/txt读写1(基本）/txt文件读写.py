with open("str_txt.txt", "w", encoding ="utf-8") as f:
    f.write("hello world")

with open("str_txt.txt", "r", encoding ="utf-8") as f:
    read = f.read()

print(read)
