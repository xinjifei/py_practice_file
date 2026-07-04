'''新建一个字典，叫 my_stock
里面放：
code：股票代码（字符串）
name：股票名称
price：价格（浮点数）
change：涨幅（浮点数）
打印：
股票名称
当前价格
把价格改成一个新价格
再打印一遍'''

my_stock = {
    "code" : "00001",
    "name" : "stack_name",
    "price" : 10.6,
    "change" : 2.5
}

print (f'stock name in <my_stock> = {my_stock["name"]}')
print (f'stock price in <my_stock> = {my_stock["price"]}')

new_price = float(input(f"enter new stock price in <my_stock>，the current price in <my_stock> = {my_stock['price']}\n>>>"))

my_stock["price"] = new_price
print(f'the price in <my_stock> have been changed to {my_stock["price"]}')

print(my_stock)

