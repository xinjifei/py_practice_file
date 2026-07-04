from huggingface_hub import snapshot_download
import os

# 模型名称（你确认的中文GPT2-355M）
model_name = "uer/gpt2-medium-chinese-cluecorpusmall"
# 保存路径（你指定的D盘文件夹）
save_path = "D:/训练/模型/chinese_gpt2_355M"

# 创建保存文件夹（避免路径不存在报错）
os.makedirs(save_path, exist_ok=True)

# 开始下载（支持断点续传）
print(f"开始下载模型 {model_name} 到 {save_path}...")
snapshot_download(
    repo_id=model_name,
    local_dir=save_path,
    resume_download=True,
    ignore_patterns=["*.git*", "*.md"]  # 忽略无关文件，加快下载
)
print("下载完成！模型文件已保存到指定路径。")