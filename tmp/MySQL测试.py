import pymysql

try:
    # 连接 MySQL
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='你设置的密码',  # 👈 替换成你安装时设置的密码
        charset='utf8mb4'
    )

    print("✅ 连接成功！")

    # 简单测试：获取数据库版本
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📦 MySQL 版本: {version[0]}")

    connection.close()

except Exception as e:
    print(f"❌ 连接失败: {e}")