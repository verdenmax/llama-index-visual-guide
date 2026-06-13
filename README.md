# LlamaIndex RAG 图解教程 · Visual Guide

[![Read online](https://img.shields.io/badge/%F0%9F%93%96-Read%20Online-1a7f64?style=for-the-badge)](https://verdenmax.github.io/llama-index-visual-guide/)
[![Download PDF](https://img.shields.io/badge/%F0%9F%93%84-Download%20PDF-b4690e?style=for-the-badge)](https://github.com/verdenmax/llama-index-visual-guide/releases/latest/download/llama-index-visual-guide.pdf)

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Lessons](https://img.shields.io/badge/lessons-21-blue.svg)
![Parts](https://img.shields.io/badge/parts-6-9cf.svg)
![Bilingual](https://img.shields.io/badge/docs-%E4%B8%AD%2FEN-orange.svg)
![Dependencies](https://img.shields.io/badge/build%20deps-none-brightgreen.svg)

一套面向新手到进阶的**可视化（HTML 图解）双语教程**，带你跟着 **RAG 数据流**
一步步理解 [LlamaIndex](https://github.com/run-llama/llama_index)：先看一份文档如何
**写入索引**（加载→切块→Embedding→存储→索引），再看一个问题如何**查出答案**
（检索→后处理→合成→回答）。每课配真实源码对应、可运行代码、设计亮点与自测题，支持
**中 / EN 一键切换**。

A bilingual, self-contained visual guide that teaches LlamaIndex RAG by following
the data flow — the **write path** then the **query path** — with real source
citations, runnable code, design insights and quizzes. Toggle 中 / EN anytime.

> 📌 对照 **llama-index-core 0.14.22** / Python 3.10+，最后核验 **2026-06**。
> 源码引用以「文件 + 符号名」为主（行号随上游更新而失效，故不写死）。

## 🚀 如何阅读 / How to read

直接用浏览器打开 **`index.html`** 即可（支持 `file://`），右上角按钮切换中 / EN：

```bash
# 可选：本地静态预览
python -m http.server 8000   # then open http://localhost:8000/
```

## 📚 教程结构（6 部分 · 21 课）

- **第一部分 · 宏观全景**：01 LlamaIndex 与 RAG 是什么 · 02 架构全景 · 03 一次 RAG 的生命周期
- **第二部分 · 写入路径**：04 Document 与 Node · 05 Readers · 06 切块 Node Parsers · 07 元数据与抽取器 · 08 Embedding · 09 向量存储 · 10 索引抽象 · 11 Ingestion 与持久化
- **第三部分 · 查询路径**：12 检索器 · 13 节点后处理 · 14 响应合成 · 15 查询引擎 · 16 聊天引擎
- **第四部分 · 进阶**：17 Settings 与 Prompt · 18 进阶检索 · 19 评估
- **第五部分 · 实战**：20 端到端 Capstone
- **第六部分 · 速查**：21 术语表 · 概念索引

## 🎨 每课包含

🌍 宏观理解 · 🧩 生活类比 · 🔬 源码对应（真实文件+符号）· 💻 可运行代码 ·
✅ 关键要点 · 💡 设计亮点 · 🧪 自测题 · 顶部进度条 + 上/下一课导航。

## 🛠️ 重新生成 / Rebuild

所有 HTML 由 `src/` 下的无依赖 Python 生成器产出（仅需 Python 3）：

```bash
cd src
python build.py          # 生成 index.html + lessons/
python build_print.py    # 生成 print.html（用于打 PDF）
```

开发期测试（需要 pytest）：`cd src && python -m pytest tests -q`。
结构校验：`python check_html.py && python check_links.py`。

### 本地导出 PDF

`print.html` 由 `build_print.py` 生成在**仓库根目录**，因此以下命令请在**仓库根目录**运行
（`chromium` 在部分系统上叫 `chromium-browser` 或 `google-chrome`）：

```bash
cd "$(git rev-parse --show-toplevel)"   # 回到仓库根目录
chromium --headless=new --no-pdf-header-footer \
  --print-to-pdf=llama-index-visual-guide.pdf \
  --virtual-time-budget=20000 "file://$PWD/print.html"
```

## 🚀 自动化（CI）

- `.github/workflows/ci.yml`：每次 push / PR 重建并校验 HTML 无漂移 + 链接 + 结构 + 单元测试。
- `.github/workflows/deploy.yml`：push 自动构建、渲染 PDF、部署 GitHub Pages；打 `v*` tag 自动发 Release 附 PDF。
- **首次启用**：仓库 Settings → Pages → Source 选 **GitHub Actions**。

## 📄 许可 / License

[MIT](./LICENSE)。本教程为独立的第三方学习材料，与 LlamaIndex / run-llama 官方无隶属关系；
相关名称与商标归各自所有者。
