huiyuan=(input('是否为会员（y/n'))
huafei=str(input('花费'))
    if huiyuan == 'y':
        if huafei > 200:

            print(f'打折后价格为{huafei*8%}')
        if huafeig