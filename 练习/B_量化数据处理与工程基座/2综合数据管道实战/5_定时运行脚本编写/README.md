#
开始

所有操作均在项目根目录中运行
power shell：
    cd #项目根目录路径#

该项目使用uv环境管理，因此使用uv进行环境对齐

#如果没有安装uv：
    power shell：
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  #安装

        uv --version#验证安装

power shell：
    uv sync #对齐环境

power shell：
    uv run ./练习题/main.py ./练习题/config.json
 #使用uv环境（.venv虚拟环境）运行主程序

 #
 配置
 
 在运行时传参参数应该指向一个.json配置文件（测试用config.json文件已经存在于./练习题/config.json）
