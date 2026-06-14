# 每课「面试官提问」设计 (Interview Questions)

**Goal:** 在每节课的自测区新增一组「面试官视角」的问题，每题配可折叠的「参考答案要点」，帮助学习者按真实技术面的标准自测与准备。

**Branch:** `interview-questions`. **Anchor:** llama-index-core 0.14.22.

---

## 1. 需求

- 范围：第 **01–20 课**（跳过 `21-glossary`，它是参考表）。
- 每课 **3–4 题**，约 70 题。
- 风格：**混合型**——概念追问 + 权衡取舍 + 场景/排查，像真实技术面，可带追问感。
- 每题配 **参考答案要点**（高分回答应覆盖哪些点），**可折叠**。
- 双语（中/EN），与全站一致。

## 2. 数据模型（`src/quizzes.py`）

在每课字典里新增可选 `"interview"` 键：

```python
"NN-file.html": {
    "mcq": [...],
    "interview": [
        {"q": L("面试官问的问题…", "interviewer's question…"),
         "answer": L("参考要点：① …；② …；③ …",
                     "Key points: (1) …; (2) …; (3) …")},
        ...
    ],
    "open": [...],
}
```

- `q`：面试官的问题（inline `<code>` 允许；非 `<pre>`，故 `&` 写 `&amp;`）。
- `answer`：参考答案要点（bilingual，要点式）。

## 3. 渲染（`src/quizzes.py` 的 `render(fname)`）

在自测区 `<div class="selftest">` 内，块顺序为：

1. **MCQ**（回忆型，已存在）
2. **🎯 面试官提问**（新增，带可折叠参考要点）
3. **💭 发散思考**（无答案，已存在）

面试块结构（复用现有 `.accordion`/`.acc-body` 样式，不新增 CSS）：

```html
<div class="quiz interview">
  <div class="qn">🎯 1. {question}</div>
  <details class="accordion">
    <summary>看参考要点 <span class="hint">点击展开</span></summary>
    <div class="acc-body"><div class="qa"><div class="a">{answer}</div></div></div>
  </details>
</div>
```

分组标题：`🎯 面试官提问 · 试着答出要点 / Interviewer asks · cover the key points`。

## 4. 不变量 / 约束

- `render()` 对没有 `"interview"` 的课保持原输出（向后兼容）。
- 仍满足 `check_html`：`<details>` 与 `<summary>` 数量配对、标签平衡、zh/en `data-lang` 块对等、无未转义 `&`/`<`。
- 构建确定性（`render` 无随机/时钟；面试题不参与 `_shuffle`）。
- PDF：`build_print.py` 会展开折叠，参考要点自动进入打印版。

## 5. 实现步骤

1. TDD：给 `render()` 加测试——含 `interview` 的课渲染出 🎯 区块、问题、可折叠要点；不含的课不变。
2. 扩展 `render()`：在 MCQ 之后、open 之前输出面试块。
3. 逐模块（part1..part5 对应的 01–20 课）撰写 `interview` Q&A：每课 3–4 题，混合风格，紧扣该课内容与真实 API。
4. 中心化校验：`build` + `check_html`(0/0) + `check_links` + `pytest` + 构建确定性。
5. 最终代码审查子代理 → 合并 `interview-questions` → `main` → 推送（触发部署）。

## 6. 成功标准

- 01–20 课每课有 3–4 道带参考要点的面试题；21 不变。
- check_html 0 错 0 警；链接全通；测试通过；构建确定性。
- 线上与 PDF 均包含面试题。
