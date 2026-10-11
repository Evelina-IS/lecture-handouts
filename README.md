```markdown
# Qwen2.5-3B-Instruct Academic Handout LoRA

基于 `Qwen/Qwen2.5-3B-Instruct` 经过 LoRA 微调的学术讲义排版生成模型。专门用于将课程课件（PDF / PPTX）的内容重构为符合规范排版、包含公式推导、例题环境及结构化章节的 A4 中文学术讲义（LaTeX `ctexart` 格式）。

---

## 目录结构

```text
├── qwen_handout_3b_lora/       # 微调后的 LoRA 适配层权重 (Git LFS)
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── ...
├── doc2handout.py              # 核心转换脚本
├── train_handout.py            # 微调训练代码
└── README.md

```

---

## 环境准备

### 1. 通用依赖安装

在各平台的 Python 环境中安装依赖包：

```bash
pip install torch transformers peft bitsandbytes pymupdf python-pptx datasets

```

### 2. LaTeX 编译环境

生成 PDF 需要使用支持中文的 XeLaTeX 引擎：

* **Ubuntu / WSL2**:
```bash
sudo apt update && sudo apt install -y texlive-xetex texlive-lang-chinese texlive-latex-extra texlive-science

```


* **macOS**:
```bash
brew install --cask mactex-no-gui

```


* **Windows**:
安装 [TeX Live](https://www.tug.org/texlive/) 或 [MiKTeX](https://miktex.org/)，确保 `xelatex` 已加入系统环境变量 `PATH`。

---

## 跨平台使用说明

### 1. Windows / WSL2

#### 步骤 1：克隆仓库（包含模型权重）

确保已安装并配置 `git-lfs`：

```bash
git lfs install
git clone [https://github.com/Evelina-IS/lecture-handouts.git](https://github.com/Evelina-IS/lecture-handouts.git)
cd lecture-handouts

```

#### 步骤 2：运行推理转换

调用 `doc2handout.py` 对课件进行处理：

```bash
python doc2handout.py /path/to/lecture.pdf 输出讲义名称

```

* 脚本自动提取文本并调用本地微调权重生成 `.tex` 源码。
* 自动调用 `xelatex` 编译生成同名 `.pdf`。

---

### 2. macOS (Apple Silicon M 系列 / Intel)

在 macOS 上若使用 MPS（Metal）加速，需将加载参数调整为纯 float16 模式（MPS 不支持 bitsandbytes 4-bit 量化）：

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

model_id = "Qwen/Qwen2.5-3B-Instruct"
lora_path = "./qwen_handout_3b_lora"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="mps",
    trust_remote_code=True
)
model = PeftModel.from_pretrained(model, lora_path)
model.eval()

```

推理生成的 `.tex` 源码使用系统终端执行编译：

```bash
xelatex -interaction=nonstopmode 输出讲义名称.tex

```

---

### 3. iPad 使用方案

iPad 操作系统受沙盒机制与框架限制，无法直接本地运行 PyTorch 及 LoRA 权重，推荐以下两种集成方案：

#### 方案 A：云端 / 本地工作站远程调用（推荐）

在运行模型的 Windows/WSL2 或 Mac 端开启轻量 API 服务（如 FastAPI），iPad 通过 **Shortcuts（快捷指令）** 上传课件文件，接收返回的 `.pdf` 直接导入 GoodNotes 或 Notability。

#### 方案 B：Git 仓库自动同步浏览

1. 在 iPad 上安装 **Working Copy**。
2. 绑定当前仓库：`https://github.com/Evelina-IS/lecture-handouts.git`。
3. 工作站端生成并推送 PDF 讲义后，在 Working Copy 中执行 `Pull`，直接点击生成的 `.pdf` 共享至笔记软件使用。

---

## 模型输出规范

本模型经过特定数据约束对齐，输出内容遵守以下排版协议：

1. 文档类必须为 `\documentclass[11pt, a4paper]{ctexart}`。
2. 导言区自动引入 `amsmath`, `amssymb`, `amsthm`, `geometry`, `booktabs`, `hyperref` 宏包。
3. 严格禁止 Beamer 幻灯片标记（如 `\frame`, `\block`），强制重构为符合正文阅读逻辑的 `\section` 与 `\subsection`。
4. 数学公式使用 `\begin{equation}` 或 `\begin{align}` 环境。
5. 计算与分析案例使用 `\begin{example}` 环境。

```

```
