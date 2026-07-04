# d55 SQLite
> 一种轻量数据库，用于快速的检索，简单操作  
> 和pandas不是替代关系，pandas用于计算操作dataframe，SQL用于大量检索、总结，优势在于语法更简单直接、快

## 使用流程概述
1. 创建db数据库文件
2. 创建连接到数据库文件
3. 操作
4. 断连数据库文件

## 具体操作
### 创建db数据库文件
```python
import os
os.path.join(os.path.dirname(__file__), "name.db")
```
### 创建连接
```python
conn = sqlite3.connect(db_path) #必创建的连接管道
cursor = conn.cursor() #游标
```

### 操作语句
- 这里如果是要对数据进行操作就需要先操作，再把数据变成dataframe输出出来。所以下面的这个函数可以把读取+操作+输出结合起来
```python
import pandas as pd
import sqlite3
#传参注释
## 第一个是解释，用来打印这个函数的具体作用
## 第二个是操作，是核心的操作，里面用SQL的独特语法来描述需要让SQL做的事情
def run_query(description:str, sql:str) ->DataFrame:
    print(description)
    #传参注释
    ##第一个就是上面说过的SQL操作语法
    ##第二个是刚才配置的数据传输参数，要是不改可以在函数体外面定义
    result = pd.read_sql_query(sql,conn)
    return result
```
- 然后就可以具体的使用这个函数区别主要就在传入的sql参数，这个是核心指令
### 举例
#### 最基础的查询
```python
run_query(
    "SELECT + WHERE — 查询贵州茅台 2024-03 的所有交易日",
    """
    SELECT date, stock_name, open, close, volume
    FROM daily_prices
    WHERE stock_name = '贵州茅台'
      AND date >= '2024-03-01'
      AND date < '2024-04-01'
    ORDER BY date
    """
)
```
### 总结主要语法
- SELECT:要有什么列
- FROM:从哪里数据（db文件的子数据）
- WHERE:筛选行
- ORDER BY:排序方式
