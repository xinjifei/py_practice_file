#时间参数函数
from datetime import datetime
import time

#耗时i计算流程>>>

#记录开始时间
start_time = datetime.now()

#随便运行点代码
time.sleep(5)
#
#
#
#

#结束时间
end_time = datetime.now()

#计算总耗时
cost_time = (end_time - start_time).total_seconds()

#格式化输出时间
print("开始时间",start_time.strftime("%Y-%m-%d %H:%M:%S"))
print("结束时间",end_time.strftime("%Y-%m-%d %H:%M:%S"))
print("总耗时=",cost_time)

#格式化规则：%后面的字母取决于需要的参数的英语首字母
