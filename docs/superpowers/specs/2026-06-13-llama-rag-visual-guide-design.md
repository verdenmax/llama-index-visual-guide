# LlamaIndex RAG 可视化教程 · 设计文档（Design Spec）

- **日期**：2026-06-13
- **作者**：@verdenmax（借助 Copilot CLI + superpowers brainstorming 生成）
- **参考项目**：`langchain-visual-guide`（同一作者的 LangChain 图解教程）
- **目标仓库**：`/home/verden/course/llama-index-visual-guide`（独立仓库，与 `langchain-visual-guide` 同级）
- **版本锚点**：对照 **llama-index-core 0.14.22 / Python 3.10+**；源码引用使用「**文件 + 符号名**」，不写死行号（行号随上游更新失效）。

---

## 1. 目标与受众（Goal & Audience）

做一套面向**新手到进阶**的可视化（自包含 HTML 图解）教程，让读者**一步一步学会整个 LlamaIndex 的 RAG 思想**。

- **核心目标**：把 RAG 的"思想"做成一条可跟随的主线——跟着"一份文档如何进库、一个问题如何出答案"两条数据流，逐步建立从"会用"到"懂原理"的完整认知。
- **受众**：
  - 完全没接触过 LlamaIndex、想从零理解 RAG 的新手；
  - 想先建立宏观认知、再深入内部源码与设计的学习者；
  - 准备阅读 / 调试 / 使用 LlamaIndex 构建 RAG 应用的开发者。
- **读者收获**：一条清晰的 RAG 数据流主线 + 每个阶段对照真实源码 + 每课可运行代码 + 一个端到端可跑的 RAG 应用 + 一份可随时查阅的术语表。

---

## 2. 范围决策（Scope Decisions）

经 brainstorming 逐项确认：

| 维度 | 决策 |
|---|---|
| **范围/深度** | 以 RAG 主链路为核心、适度延展，约 20 课（+ 术语表）。 |
| **存放位置** | 独立仓库 `/home/verden/course/llama-index-visual-guide`（与 `langchain-visual-guide` 同级）。 |
| **构建系统** | 完整镜像参考项目：无依赖 Python 生成器 + quizzes + glossary + 链接/HTML 校验 + GitHub Actions 自动部署 Pages 与生成 PDF。 |
| **语言** | **中英双语**，**页面语言切换按钮**（同一课可切 中/英 两套完整内容，`localStorage` 记忆，默认中文）。 |
| **内容侧重** | 概念讲透 **+** 每课附可运行代码片段 **+** 端到端 capstone。 |
| **课程组织** | **方案 A**：按 RAG 数据流（写入路径 → 查询路径）组织。 |

---

## 3. 技术架构（Architecture）

### 3.1 项目结构

```
llama-index-visual-guide/
├── index.html                 ← 目录页（入口），生成产物
├── lessons/                   ← NN-*.html 各课，生成产物
├── print.html                 ← PDF 源（折叠全展开），生成产物
├── src/                       ← 无依赖 Python 3 生成器（可重建全部 HTML / PDF）
│   ├── shell.py               设计系统(CSS) + 导航 + 语言切换按钮 + index 页 + page()
│   ├── i18n.py                双语基础设施：L(zh, en) 内容块封装与渲染
│   ├── part1.py … part5.py    各部分课程内容（每课提供 zh + en 两套）
│   ├── glossary.py            术语表（双语）
│   ├── quizzes.py             每课测验（双语）
│   ├── registry.py            文件名 → 课程内容 的统一映射（build 与 build_print 共用）
│   ├── build.py               站点构建（→ index.html + lessons/）
│   ├── build_print.py         PDF 源构建（→ print.html，折叠全展开）
│   ├── check_links.py         内部链接死链校验
│   └── check_html.py          HTML 结构 / 双语一致性校验
├── .github/workflows/
│   ├── deploy.yml             CI：构建 → 渲染 PDF → 部署 Pages →（tag）发 Release
│   └── ci.yml                 防回归：重建校验无漂移 + 链接校验 + HTML 校验
├── README.md                  双语简介 + 徽章 + 课程结构 + 重建/部署说明
└── LICENSE                    MIT
```

设计原则：每个 `src/*.py` 单一职责、通过明确接口（`registry.CONTENT`、`shell.PAGES`、`i18n.L`）协作，可独立理解与替换。页面之间用相对链接互联，支持 `file://` 直接打开与任意静态服务器 / GitHub Pages。无第三方依赖（仅需 Python 3）。

### 3.2 双语切换机制（核心新增，相对参考项目）

- **内容模型**：每个文本块用 `i18n.L(zh="...", en="...")` 封装。生成时**同页同时输出中/英两套** DOM，分别标注 `data-lang="zh"` / `data-lang="en"`。
- **切换 UI**：顶栏放一个 **中 / EN 切换按钮**。
- **切换逻辑**：一小段内联 JS 读取 `localStorage` 中的语言偏好（默认 `zh`），显示当前语言的 `data-lang` 块、隐藏另一语言；点击按钮切换并写回 `localStorage`；同步更新 `<html lang>`、`document.title`、导航与进度条文案。
- **约束**：纯静态、无构建期依赖、`file://` 直接可用；JS 不可用时降级为默认显示中文（英文块用 CSS 也可隐藏，保证不会双语同时堆叠）。

### 3.3 版本锚点与源码引用约定

- 对照 **llama-index-core 0.14.22 / Python 3.10+**，最后核验于 **2026-06**。
- 源码引用统一写「**文件 + 符号名**」，例如 `node_parser/text/sentence.py · SentenceSplitter`；**不写死行号**。
- 所有类名 / 方法名 / 模块路径以仓库 `llama-index-core/llama_index/core/**` 真实符号为准，实现时逐一核对。

---

## 4. 课程地图（Curriculum，方案 A：按 RAG 数据流）

共 **21 页 = 20 课 + 术语表**，分 6 部分。每课对照真实源码并附可运行代码。

### 第一部分 · 宏观全景
1. **LlamaIndex 与 RAG 是什么** — 为什么需要 RAG（知识截止 / 幻觉 → 外挂知识）· 核心心智模型。
2. **架构全景** — `core` + 300+ 集成分层；`llama_index.core.*`（核心）vs `llama_index.xxx.*`（集成）的命名约定。
3. **一次 RAG 的生命周期** — 5 行代码跑通（`SimpleDirectoryReader` → `VectorStoreIndex.from_documents` → `as_query_engine` → `query`）；写入路径 vs 查询路径全景数据流。

### 第二部分 · 写入路径（把知识装进去）
4. **Document 与 Node 数据模型** — `Document` / `TextNode` / `BaseNode` · relationships · metadata · `ref_doc_id`。来源：`schema.py`。
5. **数据加载 Readers** — `SimpleDirectoryReader` · LlamaHub readers · 产出 `Document`。来源：`readers/`。
6. **切块 Node Parsers / Splitters** — `SentenceSplitter` / `TokenTextSplitter` / `SemanticSplitterNodeParser` / `SentenceWindowNodeParser` · chunk_size / overlap 思想与权衡。来源：`node_parser/text/`。
7. **元数据与抽取器 Metadata & Extractors** — `TitleExtractor` / `KeywordExtractor` / `QuestionsAnsweredExtractor` · metadata 如何帮助检索。来源：`extractors/`。
8. **Embedding 向量化** — `BaseEmbedding` · `Settings.embed_model` · 语义相似检索原理。来源：`base/embeddings/` 与 `embeddings/`。
9. **向量存储 Vector Stores** — `VectorStoreIndex` / `SimpleVectorStore` · 集成（Chroma / FAISS …）· 存了什么。来源：`vector_stores/`。
10. **索引 Index 抽象** — `VectorStoreIndex` vs `SummaryIndex` / `DocumentSummaryIndex` / `PropertyGraphIndex` 概览 · index 到底是什么。来源：`indices/`。
11. **Ingestion Pipeline 与持久化** — `IngestionPipeline` / transformations / cache / dedup · `StorageContext` / docstore / index store / vector store / `persist` / `load`。来源：`ingestion/`、`storage/`。

### 第三部分 · 查询路径（把答案查出来）
12. **检索器 Retrievers** — `VectorIndexRetriever` · top-k / similarity · `index.as_retriever()`。来源：`indices/vector_store/retrievers/`、`base/base_retriever.py`。
13. **节点后处理 Node Postprocessors** — `SimilarityPostprocessor` · rerank · `MetadataReplacementPostProcessor`（配合 sentence window）。来源：`postprocessor/`。
14. **响应合成 Response Synthesizers** — `refine` / `compact` / `tree_summarize` / `accumulate` · context → answer 的几种策略。来源：`response_synthesizers/`。
15. **查询引擎 Query Engine** — `RetrieverQueryEngine` 把 retriever + postprocessor + synthesizer 串起来 · `as_query_engine()`。来源：`query_engine/`。
16. **聊天引擎 Chat Engine** — `ContextChatEngine` / `CondenseQuestionChatEngine` · 多轮 RAG 与记忆。来源：`chat_engine/`、`memory/`。

### 第四部分 · 进阶
17. **全局配置 Settings 与 Prompt** — `Settings`（取代 `ServiceContext`）：llm / embed_model / node_parser … · `PromptTemplate` / `ChatPromptTemplate`。来源：`settings.py`、`prompts/`。
18. **进阶检索** — 融合 `QueryFusionRetriever` · 自动合并 `AutoMergingRetriever` · 递归 `RecursiveRetriever` · 路由 `RouterRetriever`。来源：`retrievers/`。
19. **评估 Evaluation** — `FaithfulnessEvaluator` / `RelevancyEvaluator` / `CorrectnessEvaluator` · 如何判断 RAG 好不好。来源：`evaluation/`。

### 第五部分 · 实战
20. **端到端 Capstone** — 从 0 拼一个可运行的本地 RAG 问答应用：load → ingest → index → persist → retrieve → rerank → synthesize → query / chat，把前面所有阶段串起来。

### 第六部分 · 速查
21. **术语表 · 概念索引** — 全书术语一句话查 + 点链接跳到对应课。

> 数量约 20，实现期可按需要小幅增删合并；课程顺序与分部固定为上表。

---

## 5. 单课内容模板（Per-Lesson Template）

每课沿用参考项目的卡片视觉，固定骨架（中英两套，经 `i18n.L(zh, en)` 输出）：

1. **🌍 宏观理解** — `<p class="lead">` 一段话讲清"这是什么、在 RAG 里处于哪一步、为什么需要"。
2. **🧩 生活类比** — `card analogy` 卡片，用日常事物类比该抽象（如"切块 = 把书拆成便利贴"）。
3. **正文讲解** — `<h2>` 分节 + 对比 `<table class="t">`（如各 splitter / 各 synthesizer 对比）。
4. **🔬 源码对应** — 指向 llama_index 真实文件 + 符号；关键处用 `details.accordion` 折叠详解（示例 / 为什么必要 / 做法与优点 / 替代方案）。
5. **💻 可运行代码** — `pre.code` 语法高亮，给**最小可跑片段**（标注所需 `pip install` 与前置 `Settings` / API key）。
6. **✅ 关键要点** — 每课小结。
7. **💡 设计亮点** — 该课最精妙的设计思想。
8. **导航与测验** — 顶部进度条 + 上一课 / 下一课导航（来自 `shell`）+ 课末测验（`quizzes.py`，双语）。

**贯穿主线（可视化"一步步"）**：每课开头用一张"RAG 管道图"高亮当前阶段：
- 写入路径 ▸ 加载 → 切块 → Embedding → 存储 → 索引
- 查询路径 ▸ 检索 → 后处理 → 合成 → 回答

---

## 6. 构建 / CI / PDF / 校验（Build & CI）

### 6.1 本地构建（无依赖，仅需 Python 3）

```bash
cd src
python build.py        # → index.html + lessons/（双语，含切换 JS）
python build_print.py  # → print.html（折叠全展开，供打 PDF）
```

### 6.2 CI 工作流（移植自参考项目，改名 llama-index-visual-guide）

- **`ci.yml`**（push / PR 防回归）：
  1. 重跑 `build.py`，校验**提交的 HTML 与 `src/` 无漂移**（漂移即失败，提示重新构建并提交）；
  2. `check_links.py` 内部链接无死链；
  3. `check_html.py` HTML 结构校验，**升级为校验中 / 英两套 `data-lang` 块齐全、语言切换按钮存在**。
- **`deploy.yml`**（push / tag 自动部署）：
  1. 安装中日韩 + emoji 字体（`fonts-noto-cjk`、`fonts-noto-color-emoji`）；
  2. `build.py` + `build_print.py`；
  3. 无头 Chrome 渲染 **PDF**；
  4. 上传 PDF 构建产物 + 组装 `_site` 上传 Pages 产物；
  5. 部署 **GitHub Pages**；打 `v*` tag 时发 **Release** 并附带 PDF。

> **Pages 首次启用（一次性）**：仓库 Owner 需在 Settings → Pages → Source 选 "GitHub Actions"。`configure-pages` 的 `enablement:true` 在私有仓库 / 权限不足时无法自动建站，只能部署到已建好的站点。

### 6.3 PDF 语言策略

`print.html` 默认导出**中文全文**（折叠全展开、自动分页）——单一、干净的 PDF；网页端保留中 / 英切换。英文 PDF 暂不做（YAGNI），如需后续再加。

### 6.4 README

双语简介 + 在线阅读 / 下载 PDF 徽章 + 课程结构（6 部分 21 页）+ 重新生成与本地导出 PDF 说明 + 自动化部署说明 + MIT 许可与"独立第三方学习材料，与官方无隶属关系"声明。

---

## 7. 不做 / 暂缓（Out of Scope · YAGNI）

- 英文 PDF（先只做中文 PDF）。
- 把教程并入上游 `run-llama/llama_index` 仓库（保持独立仓库）。
- 深入 Agent / Workflow、多模态、PropertyGraph 内核等（仅在第 10 课做"索引类型概览"级别提及，不展开成课）。
- 任何需要第三方 Python 库才能构建站点的方案（构建期保持零依赖）。

---

## 8. 成功标准（Success Criteria）

1. `cd src && python build.py` 与 `python build_print.py` 零依赖跑通，产出 `index.html`、`lessons/`（21 页）、`print.html`。
2. 浏览器（含 `file://`）打开 `index.html`：导航、进度条、上一课 / 下一课、课末测验、**中 / EN 切换（localStorage 记忆）** 均正常。
3. 21 页内容齐全：每课含 宏观 / 类比 / 正文 / 源码对应 / 可运行代码 / 要点 / 设计亮点 / 测验，且**中英两套内容均完整**。
4. 所有源码引用（文件 + 符号）经核对在 llama-index-core 0.14.22 真实存在。
5. `check_links.py`、`check_html.py` 通过；CI 中"HTML 无漂移"校验通过。
6. capstone（第 20 课）给出的端到端代码逻辑自洽、可作为真实 RAG 应用骨架运行。
7. `deploy.yml` 能在 CI 渲染出中文正常显示的 PDF 并部署 Pages（首次需 Owner 手动启用 Pages）。
