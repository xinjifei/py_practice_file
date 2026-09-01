import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
import tqdm
import jieba

# ===================== 1. 基础配置（纯CPU） =====================
device = torch.device("cpu")  # 强制CPU运行
model_name = "gpt2"  # 基础模型（小体量，适合CPU）
batch_size = 2  # 极小批次（CPU内存有限，别调大）
epochs = 3  # 训练轮数（CPU慢，少跑几轮看效果）
learning_rate = 5e-5  # 学习率
max_seq_len = 128  # 最大序列长度（控制显存/内存占用）
corpus_path = "D:/语料/yvliao2.txt"  # 你的语料路径

# ===================== 2. 加载分词器和模型（关键替换部分） =====================
# 从本地加载GPT-2分词器（替换网络加载）
tokenizer = GPT2Tokenizer.from_pretrained("D:\\PythonProject\\.idea\\模型训练测试\\cpu_llm_model")  # 本地路径
# GPT-2默认没有<|endoftext|>之外的特殊token，补充padding token
tokenizer.pad_token = tokenizer.eos_token  # 用eos_token替代pad_token

# 从本地加载GPT-2模型（替换网络加载）
model = GPT2LMHeadModel.from_pretrained("D:\\PythonProject\\.idea\\模型训练测试\\cpu_llm_model").to(device)  # 本地路径

# ===================== 3. 加载/处理中文语料 =====================
# 加载本地txt语料（替换原来的在线语料加载）
def load_local_txt_corpus(file_path):
    """读取本地txt文件，返回文本列表"""
    texts = []
    try:
        # 读取txt文件（中文用utf-8编码，若乱码可换gbk）
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:  # 跳过空行
                    texts.append(line)
        print(f"成功加载本地语料：{file_path}，共{len(texts)}行文本")
    except Exception as e:
        print(f"加载语料失败：{e}")
        texts = []
    return texts

# 调用函数加载本地txt语料（corpus_path是你在基础配置区定义的路径）
corpus_texts = load_local_txt_corpus(corpus_path)

# 如果是一问一答格式，取消下面注释并适配（根据你的语料选择是否开启）
# formatted_texts = []
# for line in corpus_texts:
#     if "|||" in line:
#         q, a = line.split("|||", 1)
#         formatted_texts.append(f"问：{q} 答：{a}")
# corpus_texts = formatted_texts

# 自定义数据集类（适配本地txt语料，删除在线语料的逻辑）
class ChineseTextDataset(Dataset):
    def __init__(self, corpus_texts, tokenizer, max_seq_len):
        # 核心修改：接收本地文本列表，而非在线dataset对象
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.texts = []
        # 遍历本地加载的文本列表（而非在线dataset的item）
        for text in corpus_texts:
            if text:
                # 中文分词（可选，GPT-2也能直接处理字符）
                seg_text = " ".join(jieba.cut(text))
                self.texts.append(seg_text)

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        # 编码文本：转为token id，截断/补齐到max_seq_len
        encoding = self.tokenizer(
            text,
            max_length=self.max_seq_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        # 语言模型训练的标签=输入（自回归训练）
        input_ids = encoding["input_ids"].squeeze()  # 去掉多余维度
        attention_mask = encoding["attention_mask"].squeeze()
        labels = input_ids.clone()  # 标签和输入一致

        return {
            "input_ids": input_ids.to(device),
            "attention_mask": attention_mask.to(device),
            "labels": labels.to(device)
        }

# 初始化数据集和数据加载器（核心修改：传入本地corpus_texts，而非dataset）
train_dataset = ChineseTextDataset(corpus_texts, tokenizer, max_seq_len)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# ===================== 4. 定义优化器和学习率调度器 =====================
optimizer = AdamW(model.parameters(), lr=learning_rate)
# 学习率预热（稳定训练）
total_steps = len(train_loader) * epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=total_steps
)


# ===================== 5. 训练函数 =====================
def train_llm(model, train_loader, optimizer, scheduler, epoch):
    model.train()
    total_loss = 0.0
    # 进度条（直观显示训练进度）
    progress_bar = tqdm.tqdm(train_loader, desc=f"Epoch {epoch + 1}")

    for batch in progress_bar:
        # 清零梯度
        optimizer.zero_grad()

        # 前向传播：输入input_ids，计算损失
        outputs = model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["labels"]
        )
        loss = outputs.loss
        total_loss += loss.item()

        # 反向传播+更新参数
        loss.backward()
        optimizer.step()
        scheduler.step()

        # 更新进度条显示
        progress_bar.set_postfix({"loss": f"{loss.item():.4f}"})

    # 打印本轮平均损失
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1} Average Loss: {avg_loss:.4f}")


# ===================== 6. 执行训练 =====================
if __name__ == "__main__":
    print("开始训练语言模型（纯CPU）...")
    for epoch in range(epochs):
        train_llm(model, train_loader, optimizer, scheduler, epoch)

    # ===================== 7. 测试生成（训练后验证效果） =====================
    print("\n训练完成，测试文本生成...")
    model.eval()  # 切换到推理模式
    # 输入提示词（比如“张无忌”）
    prompt = "张无忌"
    # 编码提示词
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    # 生成文本（CPU版速度慢，参数调保守）
    outputs = model.generate(
        **inputs,
        max_length=50,  # 生成最大长度
        num_return_sequences=1,
        no_repeat_ngram_size=2,  # 避免重复
        temperature=0.7,  # 随机性
        pad_token_id=tokenizer.eos_token_id
    )
    # 解码并打印生成结果
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"提示词：{prompt}")
    print(f"生成文本：{generated_text}")

    # 保存训练后的模型
    model.save_pretrained("./cpu_llm_model")
    tokenizer.save_pretrained("./cpu_llm_model")
    print("\n模型已保存到 ./cpu_llm_model 文件夹")