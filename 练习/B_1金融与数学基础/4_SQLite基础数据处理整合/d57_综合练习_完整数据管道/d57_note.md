# d57 完整数据分析流程
> 把前面学过的串起来，写出、总结出量化分析的全流程
## 写代码
*代码位置./d57_pipeline_pracrice.py*

### quick start
```bash
cd D:\PY_practice_file\练习\4_SQLite基础数据处理整合
uv run .\d57_综合练习_完整数据管道\d57_pipeline_pracrice.py
```

## 总结
### 全流程图
```
akshare数据源
↓
写入SQL数据库
↓
SQL库 读回/检索 数据
↓
pandas等工具分析数据
↓
plotly可视化显示结果
```