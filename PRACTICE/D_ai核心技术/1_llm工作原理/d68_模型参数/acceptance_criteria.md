# 第 68 天验收标准

## 体系定位
- 所处阶段：阶段四「AI 核心技术」› LLM 工作原理（概念层面，零PyTorch），第 3/4 天。
- 前面铺了什么：d66 Token（模型的输入单位）、d67 Embedding（token 变成语义坐标）——学的是模型"怎么读"和"怎么懂"。
- 今天的概念：模型"怎么被控制"。Context Window / Temperature / Top-P 是三个旋钮，决定记忆长度和输出风格。
- 和目标的关系：技术判断力的拼图——以后模型输出"不好"，你要能判断是 prompt 的问题还是参数的问题，以及该往哪个方向拧。

## AI 分界线
- **归你（必须长在脑子里）**：
  - Context Window = 短期记忆上限，超了就"忘记"最早的内容
  - Temperature 控制创造性 vs 确定性，什么任务用低 / 高
  - Top-P 和 Temperature 都是采样控制，为什么通常只调一个
- **可外包（概念要知道、实现交给 AI）**：
  - 具体 API 调用代码（base_url、messages 结构）
  - 内部采样数学（概率分布 / softmax / 截断）
  - 精确参数值（0.2 还是 0.3 的差别）

## 硬线（不过不能结束，达标看 note.md 写没写到位）
- [ ] 硬线1：能说清 Context Window 是什么——模型的短期记忆上限，超了会发生什么（最早的内容被"遗忘"）
- [ ] 硬线2：能说清 Temperature 控制什么——0 死板确定、1 平衡、>1 天马行空，并能各举一个"该用低 / 高 temperature"的任务
- [ ] 硬线3：能说清 Top-P 是什么、和 Temperature 的关系——都是控制随机性的采样方法，通常只调一个

## 代码练习（少量，仅当硬线涉及动手写代码）
- [ ] 用 DeepSeek API 写脚本：同一个 prompt 跑 temperature=0 / 0.7 / 1.5（各 2~3 次观察重复性），再固定 temperature 跑 top_p 对比。参考 demo_parameters.py，但 prompt 换成你自己的

## 软线（可选）
- [ ] Context Window 超限时 API 的具体报错和 token 计数——知道"会忘"即可，实际调试交给 AI
