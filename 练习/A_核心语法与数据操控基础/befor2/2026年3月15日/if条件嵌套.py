vip=input('是否有VIP（y/n）')
xiaofeijine=int(input('消费金额='))

if vip == 'y':
    if xiaofeijine >= 200:
        print('消费金额为',xiaofeijine*0.8)
    elif xiaofeijine >= 100:
        print('消费金额为', xiaofeijine * 0.9)
    else:
        print(f'消费金额为{xiaofeijine}')

else:
    print(f'消费金额为{xiaofeijine}')





