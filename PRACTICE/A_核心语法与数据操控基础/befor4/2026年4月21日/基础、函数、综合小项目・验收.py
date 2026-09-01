stocks = [
    {"name": "平安银行", "cost": 12.35, "price": 13.12, "hold": 800},
    {"name": "万科A", "cost": 10.22, "price": 9.87, "hold": 500},
    {"name": "贵州茅台", "cost": 1725, "price": 1806, "hold": 100},
    {"name": "五粮液", "cost": 158.6, "price": 165.2, "hold": 300},
    {"name": "格力电器", "cost": 34.6, "price": 33.9, "hold": 600},
    {"name": "美的集团", "cost": 52.8, "price": 55.4, "hold": 400},
    {"name": "海尔智家", "cost": 23.1, "price": 24.5, "hold": 700},
    {"name": "比亚迪", "cost": 235, "price": 248, "hold": 200},
    {"name": "宁德时代", "cost": 182, "price": 190, "hold": 200},
    {"name": "立讯精密", "cost": 32.4, "price": 33.8, "hold": 500},
    {"name": "隆基绿能", "cost": 28.6, "price": 27.9, "hold": 600},
    {"name": "通威股份", "cost": 26.3, "price": 25.5, "hold": 500},
    {"name": "长江电力", "cost": 24.8, "price": 25.3, "hold": 800},
    {"name": "中国神华", "cost": 30.2, "price": 31.5, "hold": 400},
    {"name": "陕西煤业", "cost": 19.4, "price": 20.8, "hold": 700},
    {"name": "招商银行", "cost": 32.6, "price": 33.9, "hold": 500},
    {"name": "兴业银行", "cost": 16.8, "price": 17.3, "hold": 900},
    {"name": "工商银行", "cost": 4.52, "price": 4.65, "hold": 2000},
    {"name": "建设银行", "cost": 5.86, "price": 6.02, "hold": 1500},
    {"name": "中国平安", "cost": 48.2, "price": 49.6, "hold": 400},
    {"name": "中国人寿", "cost": 32.5, "price": 33.8, "hold": 500},
    {"name": "中信证券", "cost": 22.4, "price": 23.1, "hold": 600},
    {"name": "东方财富", "cost": 16.8, "price": 17.5, "hold": 800},
    {"name": "同花顺", "cost": 118, "price": 125, "hold": 200},
    {"name": "海康威视", "cost": 34.2, "price": 35.6, "hold": 400},
    {"name": "大华股份", "cost": 14.3, "price": 15.1, "hold": 700},
    {"name": "恒瑞医药", "cost": 42.8, "price": 44.2, "hold": 300},
    {"name": "迈瑞医疗", "cost": 292, "price": 305, "hold": 100},
    {"name": "药明康德", "cost": 68.5, "price": 71.2, "hold": 200},
    {"name": "爱尔眼科", "cost": 28.4, "price": 29.6, "hold": 500},
    {"name": "片仔癀", "cost": 225, "price": 236, "hold": 100},
    {"name": "云南白药", "cost": 52.6, "price": 54.2, "hold": 300},
    {"name": "长春高新", "cost": 132, "price": 138, "hold": 200},
    {"name": "沃森生物", "cost": 32.8, "price": 31.5, "hold": 400},
    {"name": "智飞生物", "cost": 42.5, "price": 44.1, "hold": 300},
    {"name": "复星医药", "cost": 36.2, "price": 37.8, "hold": 400},
    {"name": "上海医药", "cost": 18.4, "price": 19.2, "hold": 600},
    {"name": "白云山", "cost": 26.8, "price": 27.9, "hold": 500},
    {"name": "同仁堂", "cost": 42.3, "price": 43.8, "hold": 300},
    {"name": "伊利股份", "cost": 28.2, "price": 29.4, "hold": 500},
    {"name": "蒙牛乳业", "cost": 32.5, "price": 33.6, "hold": 400},
    {"name": "海天味业", "cost": 42.8, "price": 44.2, "hold": 300},
    {"name": "中炬高新", "cost": 32.4, "price": 31.5, "hold": 400},
    {"name": "千禾味业", "cost": 18.6, "price": 19.4, "hold": 600},
    {"name": "涪陵榨菜", "cost": 22.8, "price": 23.9, "hold": 500},
    {"name": "绝味食品", "cost": 32.5, "price": 33.8, "hold": 400},
    {"name": "天味食品", "cost": 16.8, "price": 17.6, "hold": 700},
    {"name": "安井食品", "cost": 82.4, "price": 85.6, "hold": 200},
    {"name": "三全食品", "cost": 18.2, "price": 19.1, "hold": 600},
    {"name": "双汇发展", "cost": 22.6, "price": 23.8, "hold": 500},
    {"name": "牧原股份", "cost": 32.8, "price": 34.2, "hold": 400},
    {"name": "新希望", "cost": 12.4, "price": 13.1, "hold": 900},
    {"name": "正邦科技", "cost": 7.23, "price": 6.89, "hold": 1200},
    {"name": "天邦食品", "cost": 6.85, "price": 7.12, "hold": 1000},
    {"name": "唐人神", "cost": 8.22, "price": 8.56, "hold": 800},
    {"name": "立华股份", "cost": 22.4, "price": 23.5, "hold": 500},
    {"name": "湘佳股份", "cost": 28.6, "price": 29.8, "hold": 400},
    {"name": "民和股份", "cost": 16.8, "price": 17.5, "hold": 700},
    {"name": "仙坛股份", "cost": 12.4, "price": 13.2, "hold": 800},
    {"name": "圣农发展", "cost": 18.2, "price": 19.3, "hold": 600},
    {"name": "华域汽车", "cost": 18.4, "price": 19.2, "hold": 600},
    {"name": "拓普集团", "cost": 42.8, "price": 44.6, "hold": 300},
    {"name": "旭升集团", "cost": 28.6, "price": 29.8, "hold": 400},
    {"name": "文灿股份", "cost": 32.4, "price": 33.8, "hold": 400},
    {"name": "爱柯迪", "cost": 16.8, "price": 17.6, "hold": 700},
    {"name": "泉峰汽车", "cost": 22.4, "price": 23.5, "hold": 500},
    {"name": "博俊科技", "cost": 28.6, "price": 29.9, "hold": 400},
    {"name": "华依科技", "cost": 42.8, "price": 44.2, "hold": 300},
    {"name": "上声电子", "cost": 32.5, "price": 33.9, "hold": 400},
    {"name": "科博达", "cost": 52.8, "price": 54.6, "hold": 200},
    {"name": "德赛西威", "cost": 82.4, "price": 85.6, "hold": 200},
    {"name": "华阳集团", "cost": 32.8, "price": 34.2, "hold": 400},
    {"name": "均胜电子", "cost": 16.8, "price": 17.5, "hold": 700},
    {"name": "宁波华翔", "cost": 12.4, "price": 13.2, "hold": 800},
    {"name": "三花智控", "cost": 22.6, "price": 23.8, "hold": 500},
    {"name": "盾安环境", "cost": 8.22, "price": 8.56, "hold": 1000},
    {"name": "银轮股份", "cost": 12.4, "price": 13.1, "hold": 800},
    {"name": "松芝股份", "cost": 16.8, "price": 17.6, "hold": 700},
    {"name": "奥特佳", "cost": 2.85, "price": 2.98, "hold": 3000},
    {"name": "春兴精工", "cost": 4.22, "price": 4.38, "hold": 2000},
    {"name": "宜安科技", "cost": 8.22, "price": 7.89, "hold": 1000},
    {"name": "祥鑫科技", "cost": 22.4, "price": 23.5, "hold": 500},
    {"name": "铭利达", "cost": 28.6, "price": 29.8, "hold": 400},
    {"name": "瑞鹄模具", "cost": 16.8, "price": 17.6, "hold": 700},
    {"name": "天汽模", "cost": 4.22, "price": 4.38, "hold": 2000},
    {"name": "成飞集成", "cost": 42.8, "price": 44.6, "hold": 300},
    {"name": "中航沈飞", "cost": 52.8, "price": 54.6, "hold": 200},
    {"name": "中航西飞", "cost": 28.6, "price": 29.8, "hold": 400},
    {"name": "中直股份", "cost": 32.4, "price": 33.8, "hold": 400},
    {"name": "洪都航空", "cost": 22.4, "price": 23.5, "hold": 500},
    {"name": "航天电器", "cost": 42.8, "price": 44.2, "hold": 300},
    {"name": "航天电子", "cost": 12.4, "price": 13.2, "hold": 800},
    {"name": "中国卫星", "cost": 22.6, "price": 23.8, "hold": 500},
    {"name": "中国海防", "cost": 32.5, "price": 33.9, "hold": 400},
    {"name": "海格通信", "cost": 12.4, "price": 13.1, "hold": 800},
    {"name": "北斗星通", "cost": 28.6, "price": 29.8, "hold": 400},
    {"name": "合众思壮", "cost": 8.22, "price": 7.89, "hold": 1000},
    {"name": "华测导航", "cost": 22.4, "price": 23.5, "hold": 500}
]



def output_f(stocks):

    all_p_l = 0
    p_l_output = []
    all_cost = 0
    p_l_list = []
    p_l_key = 0
    max_abs = 0
    max_str = ""

    for stock in stocks:
        p_l = stock["price"] * stock["hold"] - stock["cost"] * stock["hold"]
        all_p_l += p_l * stock["hold"]
        p_l_output.append(f"名称={stock['name']}，盈亏={p_l:.3f}")
        p_l_list.append(p_l)
        all_cost += stock["cost"] * stock["hold"]

        if p_l_key ==0:
            max_abs = abs(p_l)
            max_str = f"盈亏绝对值最大的一只股票={stock['name']}(盈亏={p_l:.3f})"

        else:
            if abs(p_l) > max_abs:
                max_abs = abs(p_l)
                max_str = f"盈亏绝对值最大的一只股票={stock['name']}(盈亏={p_l:.3f})"

        p_l_key += 1

    p_l_rate = all_p_l / all_cost * 100

    return p_l_output, all_p_l, p_l_rate, max_str

result= output_f(stocks)

print("显示总盈亏值>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
for p_l_line in result[0]:
    print(p_l_line)
print("\n显示总盈亏额>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(f"总盈亏额={result[1]:.2f}")
print("\n显示总收益率>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(f"总收益率={result[2]:.2f}%")
print("\n显示拥有最大盈亏额绝对值的股票>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(result[3])




