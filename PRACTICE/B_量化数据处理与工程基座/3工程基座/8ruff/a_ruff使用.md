# ruff 使用
## ruff的作用
- 找出低级错误
    - 变量名未饮用
    - 函数传的参数没对上
    - 库未引用
- 让代码更干净
    - 更加符合规范，但是不致命的问题
- 让ai快速排查问题
    - 省token

## ruff的基本命令
### 使用重点
这是python库不是全局工具不能直接`ruff <somthing>`,必须要加上`uv run`然后再`ruff <somthing>`    
### 命令
- 使用`ruff check .`发现问题
    - 大部分时候要用`ruff check . --select=ALL
`要不然默认发现不了啥问题
- 使用`ruff format .`来修复问题
    - 但是只能修复一些基本问题，比如排版啥的

## ruff在项目中的基本使用流程
1. 写完一个功能
2. `uv run ruff format .`
3. `uv run ruff check . --select=ALL`
4. 修干净
5. `git add .` 然后确认一下 `git commit -m "<说明>"`
