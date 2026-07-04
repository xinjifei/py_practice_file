#格式：（【变量名】=input(【提示词】)）

#例

#求双几何图形公共重心
tx1_mj=int(input('tx1_mj='))
tx1_zb_x=int(input('tx1_zb_x='))
tx1_zb_y=int(input('tx1_zb_y='))

tx2_mj=int(input('tx2_mj='))
tx2_zb_x=int(input('tx2_zb_x='))
tx2_zb_y=int(input('tx2_zb_y='))

yunsuan_x=(tx1_mj*tx1_zb_x+tx2_mj*tx2_zb_x)/(tx1_mj+tx2_mj)
print(f'yunsuan_x={yunsuan_x}')

yunsuan_y=(tx1_mj*tx1_zb_y+tx2_mj*tx2_zb_y)/(tx1_mj+tx2_mj)
print(f'yunsuan_y={yunsuan_y}')

print(f'组合图形重心坐标为（x{yunsuan_x},y{yunsuan_y})')




