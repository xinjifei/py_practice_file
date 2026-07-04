import torch
import os
from torch.utils.data import Dataset, DataLoader
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
import tqdm
import jieba
import warnings

# 忽略无关警告（jieba语法警告、transformers版本警告）
warnings.filterwarnings("ignore")

# ===================== 1. 核心配置（适配逍遥行GPT2基础版） =====================
# 自动检测GPU/CPU，优先用GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"✅ 当前使用设备：{device}")

# 逍遥行中文GPT2（基础版）专属配置
model_hf_name = "uer/gpt2-chinese-cluecorpussmall"  # 模型官方标识
local_model_path = "D:/PythonProject/.idea/模型训练测试/cpu_llm_model"  # 本地保存路径
local_model_path = os.path.abspath(local_model_path).replace("\\", "/")  # 标准化路径

# 训练参数（适配该模型的最优参数）
batch_size = 16 if torch.cuda.is_available() else 2  # GPU批次拉满，CPU保守
epochs = 5  # 基础版模型训练收敛快
learning_rate = 5e-5  # 官方推荐学习率
max_seq_len = 256  # 基础版可支持更长序列
corpus_path = "D:/语料/yvliao2.txt"  # 你的语料路径


# ===================== 2. 一键下载+加载逍遥行中文GPT2（基础版） =====================
def load_uer_gpt2(local_path):
    """下载并加载逍遥行中文GPT2（基础版）"""
    # 检查本地是否已有模型，无则自动下载
    if not os.path.exists(local_path) or not os.listdir(local_path):
        print(f"📥 本地无模型，自动下载【逍遥行中文GPT2基础版】到：{local_path}")
        # 下载官方预训练模型
        tokenizer = GPT2Tokenizer.from_pretrained(model_hf_name)
        model = GPT2LMHeadModel.from_pretrained(model_hf_name)
        # 保存到本地
        os.makedirs(local_path, exist_ok=True)
        tokenizer.save_pretrained(local_path)
        model.save_pretrained(local_path)
        print("✅ 模型下载完成！")
    else:
        print(f"🔧 从本地加载【逍遥行中文GPT2基础版】")
        # 从本地加载
        tokenizer = GPT2Tokenizer.from_pretrained(
            local_path,
            local_files_only=True,
            trust_remote_code=True
        )
        model = GPT2LMHeadModel.from_pretrained(
            local_path,
            local_files_only=True,
            trust_remote_code=True
        )

    # 关键配置：设置pad token（GPT2默认无，必须补充）
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.pad_token_id

    # 移到GPU/CPU
    model = model.to(device)
    return tokenizer, model


# 执行加载
tokenizer, model = load_uer_gpt2(local_model_path)


# ===================== 3. 加载中文语料 =====================
def load_local_txt_corpus(file_path):
    """读取本地txt语料，兼容utf-8/gbk编码"""
    texts = []
    encodings = ["utf-8", "gbk"]  # 优先utf-8，失败则试gbk
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 5:  # 过滤空行和过短文本
                        texts.append(line)
            print(f"✅ 语料加载成功（编码：{encoding}），共{len(texts)}条文本")
            break
        except Exception as e:
            if encoding == encodings[-1]:  # 最后一种编码也失败
                print(f"❌ 语料加载失败：{e}")
    return texts


# 加载你的语料
corpus_texts = load_local_txt_corpus(corpus_path)
if not corpus_texts:
    raise ValueError("⚠️ 语料加载为空，请检查文件路径或文件内容！")


# ===================== 4. 自定义数据集（适配中文） =====================
class ChineseTextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_seq_len):
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len
        self.encodings = []

        # 预处理文本：分词+编码
        for text in tqdm.tqdm(texts, desc="📝 预处理文本"):
            # 中文分词（逍遥行GPT2适配分词后的文本）
            seg_text = " ".join(jieba.cut(text))
            # 编码为token id
            encoding = self.tokenizer(
                seg_text,
                max_length=max_seq_len,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )
            self.encodings.append({
                "input_ids": encoding["input_ids"].squeeze(),
                "attention_mask": encoding["attention_mask"].squeeze(),
                "labels": encoding["input_ids"].squeeze().clone()
            })

    def __len__(self):
        return len(self.encodings)

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings[idx]["input_ids"].to(device),
            "attention_mask": self.encodings[idx]["attention_mask"].to(device),
            "labels": self.encodings[idx]["labels"].to(device)
        }


# 初始化数据集和数据加载器
train_dataset = ChineseTextDataset(corpus_texts, tokenizer, max_seq_len)
train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=0 if torch.cuda.is_available() else 0  # GPU下关闭多线程避免报错
)

# ===================== 5. 优化器和学习率调度器 =====================
optimizer = AdamW(
    model.parameters(),
    lr=learning_rate,
    eps=1e-8,
    weight_decay=0.01  # 防止过拟合
)
total_steps = len(train_loader) * epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=int(total_steps * 0.1),  # 10%步数预热
    num_training_steps=total_steps
)

# ===================== 6. 训练函数（带GPU混合精度） =====================
# 混合精度训练（GPU加速）
scaler = torch.cuda.amp.GradScaler() if torch.cuda.is_available() else None


def train_model(model, loader, optimizer, scheduler, epoch):
    model.train()
    total_loss = 0.0
    progress_bar = tqdm.tqdm(loader, desc=f"Epoch {epoch + 1}/{epochs}")

    for batch in progress_bar:
        optimizer.zero_grad()

        # 前向传播（混合精度）
        if scaler:
            with torch.cuda.amp.autocast():
                outputs = model(
                    input_ids=batch["input_ids"],
                    attention_mask=batch["attention_mask"],
                    labels=batch["labels"]
                )
                loss = outputs.loss
        else:
            outputs = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                labels=batch["labels"]
            )
            loss = outputs.loss

        total_loss += loss.item()

        # 反向传播
        if scaler:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        scheduler.step()
        progress_bar.set_postfix({"loss": f"{loss.item():.4f}"})

    avg_loss = total_loss / len(loader)
    print(f"📊 Epoch {epoch + 1} 平均损失：{avg_loss:.4f}")
    return avg_loss


# ===================== 7. 执行训练 =====================
if __name__ == "__main__":
    print("\n🚀 开始训练【逍遥行中文GPT2基础版】...")
    for epoch in range(epochs):
        avg_loss = train_model(model, train_loader, optimizer, scheduler, epoch)

    # ===================== 8. 测试生成 =====================
    print("\n🎉 训练完成！测试文本生成：")
    model.eval()  # 切换到推理模式
    prompt = "张无忌"  # 自定义提示词
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 生成文本（适配逍遥行GPT2的生成参数）
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=150,  # 生成长度
            num_return_sequences=1,
            no_repeat_ngram_size=2,  # 避免重复
            temperature=0.7,  # 随机性
            top_k=50,  # 采样Top-K
            top_p=0.9,  # 采样Top-P
            pad_token_id=tokenizer.eos_token_id
        )

    # 解码并打印结果
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"🔍 提示词：{prompt}")
    print(f"📝 生成文本：{generated_text}")

    # ===================== 9. 保存训练后的模型 =====================
    model.save_pretrained(local_model_path)
    tokenizer.save_pretrained(local_model_path)
    print(f"\n💾 训练后的模型已保存到：{local_model_path}")