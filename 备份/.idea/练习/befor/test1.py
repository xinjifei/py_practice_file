from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model
from datasets import Dataset
import torch

# 1. 加载小体积Qwen模型（适合新手）
model_name = "Qwen/Qwen2.5-0.6B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

# 2. 处理语料：将整理好的语料转换成模型可识别格式
oral_corpus = [
    {"user": "今天天气怎么样", "response": "害，今天这天气别提了，风大得很，出门可得裹严实点"},
    # 此处添加更多语料
]
# 转换为Dataset格式，添加对话模板
def format_func(examples):
    texts = []
    for user, resp in zip(examples["user"], examples["response"]):
        # 适配Qwen对话格式
        text = tokenizer.apply_chat_template(
            [{"role": "user", "content": user}, {"role": "assistant", "content": resp}],
            tokenize=False, add_generation_prompt=False
        )
        texts.append(text)
    return {"text": texts}
dataset = Dataset.from_list(oral_corpus).map(format_func)

# 3. 配置QLoRA参数
lora_config = LoraConfig(
    task_type="CAUSAL_LM",
    r=8,  # 秩，显存小就设8，大则设16
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Qwen固定目标模块
    lora_alpha=16,
    lora_dropout=0.1
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # 查看可训练参数

# 4. 设置训练参数
training_args = TrainingArguments(
    output_dir="./qwen_oral_finetune",  # 模型保存路径
    learning_rate=5e-5,  # 学习率，不用改
    per_device_train_batch_size=1,  # 批次大小，显存小设1
    num_train_epochs=3,  # 训练轮次，3轮足够
    logging_steps=10
)

# 5. 启动训练
trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
# 保存微调后的适配器
model.save_pretrained("./qwen_oral_adapter")