# 📚 Lecture Handouts & Academic Notes

本仓库用于同步由本地 AI 模型自动生成的 **A4 学术排版讲义**（涵盖金融学、计算机体系结构及各类专业课），支持在 **iPad**、**Mac** 和 **Windows** 间无缝同步与阅读。

---

## 📱 iPad 使用指南

### 方式 1：Safari 浏览器直存（最便捷）
1. 打开 Safari 访问仓库：`https://github.com/Evelina-IS/lecture-handouts`
2. 点击目标文件（如 `.pdf` 或 `.tex`），点击 **Download raw file**。
3. 点击右上角 **分享图标** $\to$ 选择 **GoodNotes / Notability / MarginNote** 即可导入手写批注。

### 方式 2：Working Copy 自动拉取
1. 在 iPad App Store 下载免费 Git 工具 **Working Copy**。
2. 点击 `+` $\to$ **Clone repository**，填入仓库地址：
   ```text
   [https://github.com/Evelina-IS/lecture-handouts.git](https://github.com/Evelina-IS/lecture-handouts.git)```
## 💻 Mac 使用指南
1. 同步与查看打开终端（Terminal）克隆仓库：Bashgit clone [https://github.com/Evelina-IS/lecture-handouts.git](https://github.com/Evelina-IS/lecture-handouts.git) ~/lecture-handouts
cd ~/lecture-handouts
git pull
2. 编译 LaTeX (.tex $\to$ .pdf)若安装了 MacTeX，可直接在终端编译：Bashxelatex -interaction=nonstopmode *.tex
## 🖥️ Windows 使用指南
1. 同步仓库在 PowerShell 或 Git Bash 中执行：PowerShellgit clone [https://github.com/Evelina-IS/lecture-handouts.git](https://github.com/Evelina-IS/lecture-handouts.git)
2. 本地查看与编译阅读与批注：直接使用 Edge、Acrobat 或 Drawboard PDF 打开 .pdf。修改与编译：可使用 VS Code（配合 LaTeX Workshop 插件）或 TeXstudio 打开 .tex 源码，选择编译器为 XeLaTeX 一键编译。⚙️ 快捷同步脚本（WSL2 / Linux 端）在生成新的讲义
