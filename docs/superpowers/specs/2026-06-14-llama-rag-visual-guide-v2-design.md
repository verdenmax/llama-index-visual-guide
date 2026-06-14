# LlamaIndex RAG 可视化教程 · v2 增强（图解 + 深度）设计文档

- **日期**：2026-06-14
- **作者**：@verdenmax（借助 Copilot CLI + superpowers brainstorming 生成）
- **前置**：v1 已完成（21 课 + 术语表，双语切换，CI/Pages/PDF）。本文件是 **v2 增强** 的设计。
- **目标仓库 / 分支**：`/home/verden/course/llama-index-visual-guide`，分支 `v2-enhance`。
- **版本锚点**：沿用 **llama-index-core 0.14.22 / Python 3.10+**。

---

## 1. 背景与目标（Why v2）

v1 审计（基于证据，对照参考项目 langchain-visual-guide）发现两处短板：

- **配图不足**：全书"图"只有每课一条 `pipeline` 像素条 + 一张对比表；参考项目用了 ~77 处真正的流程图/分层图/示意图（flow/vflow/layer/mockup/cols），我们这类图 = 0。
- **深度偏简**：每课正文可见文字 ~2,900–4,300 字符（参考 ~4,600–8,066，约为其 55–65%）；只有 1 段流式正文、1 张表、1 段代码，无内部机制展开、无可折叠深挖、无多例子。

**v2 目标**：把它升级成真正的"**图解 + 详尽**"教程：
- 每课 **2–3 张真正的图**（HTML/CSS 为主，个别几何用内联 SVG），图里文字双语随切换；
- 每课加 **可折叠深挖**（示例 / 为什么这么设计 / 内部怎么跑 / 替代方案）与 **第 2 个代码例子**；
- 文字体量 **对齐或超过参考项目（~6–8k 字符/课）**；
- 全书新增约 **40+ 张图**。

**不变的约束**：构建期零第三方依赖；双语 `L(zh,en)` + 中/EN 一键切换；`check_html`/`check_links` 全绿；构建幂等；源码引用真实可核。

---

## 2. 范围决策（已与用户确认）

| 维度 | 决策 |
|---|---|
| 丰富度档位 | 每课 2–3 张图 + 可折叠深挖 + 多例子，文字 ~6–8k 字符（对齐/超过参考） |
| 图技术 | **方案 C**：HTML/CSS 图为主，个别需要几何的用少量内联 SVG；标签均经 `L(zh,en)` 双语 |
| 现有 `pipeline` 条 | 保留（每课顶部"阶段定位器"），新图为额外讲解配图 |
| 范围 | 全面 v2，21 课全部增强；术语表(L21)只做轻量增强（不强加图） |

---

## 3. 图组件系统（新增 `src/diagrams.py`）

一套**可复用、双语**的 HTML/CSS 图原语；CSS 追加到 `shell.EXTRA_CSS`（或独立 `DIAGRAM_CSS` 由 shell 引入）。每个原语单一职责、返回 HTML 字符串、接受 `L`/str、可单测。

| 原语 | 签名（约定） | 画什么 |
|---|---|---|
| `flow` | `flow(steps, active=None, label=None)` | 一排**方块 + 箭头**横向流程；`steps`=[(key, title_L, note_L?)]；可高亮一个 key |
| `vflow` | `vflow(stages)` | **纵向**数据变换流（上→下 + ↓箭头）；`stages`=[(title_L, produces_L?)] |
| `layers` | `layers(rows, caption=None)` | **分层堆叠**；`rows`=[(label_L, items_L?)]，自上而下 |
| `annot` | `annot(center_L, callouts)` | **带标注**的中心物 + 四周标签；`callouts`=[(label_L, desc_L)] |
| `compare2` | `compare2(left, right)` | **左右对照**双栏；`left/right`=(title_L, body_html) |
| `grid` | `grid(headers, cells)` | **可视化网格/矩阵**（比表格更图形，带色块/图标） |
| `scatter` | `scatter(doc_pts, query_pt, k=3, caption=None)` | **向量空间散点**（唯一内联 SVG）：文档点 + 查询点 + 最近邻圈；坐标在源码里给定，标签为 DOM 文本 |

实现要点：
- 纯 HTML/CSS；`scatter` 是一小段内联 SVG（点/圈用 `<circle>`，**文字标签放在外层 HTML** 以便双语；或 SVG `<text>` 仅放无需翻译的数字/字母）。
- 复用绿色卡片设计系统；新增类（统一进 `EXTRA_CSS`）：`.fig`（图容器+图注）、`.fbox`/`.farrow`/`.frow`（flow）、`.fvrow`/`.fvarrow`（vflow）、`.flayer`（layers）、`.fannot`/`.fcall`（annot）、`.fcol`（compare2）、`.fgrid`（grid）、`.fscatter`（scatter）。
- 每张图可带一句**图注** `caption`（`L`），双语。
- 所有图文字经 `i18n.render`，`check_html` 的双语/转义/标签平衡校验照常生效（图里也不能有裸 `&`/`<`）。
- 响应式 + 打印友好：窄屏与 PDF 下用 `flex-wrap`/降级竖排；`break-inside: avoid`（在 `build_print.py` 的 PRINT_CSS 已对 `.fig` 加规则）。

模块边界：`diagrams.py` 仅依赖 `i18n`（与 `components.py` 同级）。`components.py` 不变；内容模块 `import diagrams as d`。

---

## 4. v2 单课深度模板

在 v1 骨架上加深加图（★ = 新增/加强）。目标每课 2–3 张图、可折叠深挖、多例子、~6–8k 字。

1. **🌍 宏观理解** — lead 扩到 2–3 句。
2. **🗺️ 主图 hero ★** — 紧跟 lead 的点题大图（本课主流程/数据变换）。
3. **🧩 生活类比** — 保留。
4. **正文分节（2–3 个 `<h2>`）★** — 单段扩成多节深讲；穿插**第 2 张图**。
5. **🔬 源码对应 + 可折叠深挖 ★** — `details.accordion`，含 **示例 · 为什么这么设计 · 内部怎么跑 · 替代方案** 四块（用 `components.accordion` + `qa_item`，终于派上用场）。
6. **💻 可运行代码** — 主例 + **第 2 个例子 ★**（进阶/变体）。
7. **（按需）第 3 张小图/标注图 ★**。
8. **✅ 关键要点** — 3–4 条。
9. **💡 设计亮点** — 保留。
10. **🧪 测验** — 保留（部分课加第 2 题）。
11. 顶部 `pipeline` 条 + 上/下一课导航 — 保留。

**原则**：图服务于理解，每张图对应正文一个关键概念，不为配图而配图。深挖 `details` 默认折叠。

---

## 5. 逐课配图地图（约 40+ 张）

每课 2–3 张，类型与内容如下（hero=主图）。

**第一部分 · 宏观**
- **L01** ① hero `flow`：写入路径(加载→切块→Embed→存储→索引) ▸ 查询路径(检索→后处理→合成→回答) 全景；② `compare2`：闭卷 LLM vs 开卷 RAG。
- **L02** ① `layers`：core(稳定抽象) / 300+ 集成(实现) 两层 + 命名约定标注；② `flow`：换 provider 只改一行（接口→实现替换）。
- **L03** ① hero `vflow`：5 行代码 ↓ 每步产出（files→Documents→Nodes→vectors→Index→Answer）；② `compare2`：写入路径 vs 查询路径。

**第二部分 · 写入路径**
- **L04** ① `annot`：一个 Node 中心 + 标注(text / metadata / relationships: SOURCE·PREV·NEXT)；② `flow`：Document → 切块 → 多个 Node（关系连线）。
- **L05** ① `flow`：多来源(文件夹/PDF/网页/DB) → Reader → 统一 Document；② `grid`：SimpleDirectoryReader 按扩展名分派解析器。
- **L06** ① hero **chunk + overlap 标注图**（`annot`/自定义：一长条文本切成多块，相邻块重叠区高亮）★核心；② sentence-window 图（单句节点 + window 上下文）。
- **L07** ① `annot`：Node + 抽取出的 metadata 标签(title/keywords/questions/summary)；② `flow`：transformations 串联(split→title→QA)。
- **L08** ① hero **`scatter`（SVG）向量空间**：文档点 + 查询点 + 最近邻圈 ★；② `flow`：text → embed_model → 向量[1536]。
- **L09** ① `flow`：近邻查询(查询向量→VectorStore→top-k)；② `compare2`：内存 SimpleVectorStore vs 生产(Chroma/FAISS/PG)。
- **L10** ① `grid`：四种 Index 的组织方式(向量近邻 / 遍历 / 文档摘要 / 图谱)；② `flow`：Index→QueryEngine 统一入口。
- **L11** ① hero `flow`：IngestionPipeline(transformations + cache + docstore 去重)；② `annot`/`layers`：persist→磁盘→load(docstore/index/vector 三件套)。

**第三部分 · 查询路径**
- **L12** ① hero `flow`：查询 → 向量化 → 索引近邻 → top-k NodeWithScore；② `annot`：top_k 旋钮(太小漏/太大噪)。
- **L13** ① `flow`：检索结果 → [过滤/重排/替换] → 喂给 LLM 的精选 Node（"质检站"）；② `compare2`：cutoff 前/后。
- **L14** ① hero `grid`/四小图：refine / compact / tree_summarize / accumulate 各自"多片段→答案"形态 ★；② `vflow`：tree_summarize 层级合并。
- **L15** ① hero `flow`：组合根 retriever + postprocessors + synthesizer → .query()；② `vflow`：一次 query 的内部时序。
- **L16** ① `compare2`：condense_question vs context 两种多轮；② `flow`：多轮(历史+新问 → 消解 → 检索 → 答)。

**第四部分 · 进阶**
- **L17** ① `layers`/`annot`：全局 Settings 面板(llm/embed/node_parser/chunk_size)；② `annot`：Prompt 模板({context_str}/{query_str} 填空)。
- **L18** ① hero fusion 图(`flow`：一问→多改写→各检索→融合排序) ★；② `vflow`/树：auto-merging(小块命中→合并父块)。
- **L19** ① `grid`：三把尺子(Faithfulness/Relevancy/Correctness 各查什么)；② `flow`：评估闭环(改动→评估→对比指标)。

**第五部分 · 实战**
- **L20** ① hero **端到端架构大图**(`flow`/`layers`：load→ingest→index→persist→retrieve→postproc→synth→query/chat→eval) ★；② `compare2`：首次建库 vs 复用(persist/load 分支)。

**第六部分 · 速查**
- **L21** 轻量增强：可选在表头加一张 mini `flow` 复习图；不强加多图。

---

## 6. 构建 / 校验 / 测试影响

- **新增** `src/diagrams.py`（图原语）+ `src/tests/test_diagrams.py`（单测）。CSS 追加到 `shell.EXTRA_CSS`（图相关类）；`build_print.py` 的 `PRINT_CSS` 加 `.fig{break-inside:avoid}` 等打印规则。
- **内容模块**逐课改写：`part1..5.py`、`glossary.py` 引入 `import diagrams as d`，按模板插入 hero/第二图/深挖 `details`/第二代码例。
- **`check_html.py` 增强（可选但推荐）**：软校验每课含 ≥2 张图（`class="fig"` 计数 ≥2，WARN 或 ERR）；术语表豁免。继续保证双语/转义/平衡/链接全绿、构建幂等。
- **测验/术语表** 数据结构不变。
- **重新生成** `index.html` / `lessons/` / `print.html`，CI 漂移校验照常。

---

## 7. 不做 / 暂缓（YAGNI）

- 不引入图表库（mermaid/d3 等）或任何第三方构建依赖。
- 不做动画/交互图（静态图为主；折叠深挖是唯一交互）。
- 不重做设计系统配色与导航；只新增图相关 CSS。
- 术语表不强加大量图。

---

## 8. 成功标准

1. 新增 `src/diagrams.py` 7 个原语，单测通过；图为纯 HTML/CSS（仅 `scatter` 含内联 SVG），零第三方依赖。
2. 21 课每课 **≥2 张图**（术语表可豁免），全书 **≥40 张图**；图文字双语随中/EN 切换。
3. 每课加入**可折叠深挖**（示例/为什么/内部/替代）与**第 2 个代码例子**；多数课正文可见文字达到 **~6–8k 字符**（对齐/超过参考项目）。
4. `check_html` 0 error、`check_links` 全绿、构建幂等、`pytest` 全绿。
5. 浏览器(含 `file://`)与 PDF 下图均正常显示、双语正常切换、打印不破版。
6. 所有新增源码引用经核对在 0.14.22 真实存在。
