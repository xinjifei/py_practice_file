"""示例"""
#先导入logging库
import logging   #内置模块，无需uv add

#配置logging输出信息
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s | %(levelname)-8s | %(message)s" #这里的信息分别为：格式化时间显示,等级显示，自定义的提示
)

#替换print
logging.debug("这里用来放自定义的提示")   #一般用来调试的时候看变量值
logging.info("函数快#function#，运行成功")    #程序运行正常的提示
logging.warning("配置#config#没找到，使用默认值")   #潜在风险
logging.error("发生错误#error_information#")   #发生明确错误
logging.critical("发生系统级错误#system_error_information#")   #发生系统级错误
