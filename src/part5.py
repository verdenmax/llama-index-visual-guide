"""Part 5 (capstone): lesson 20. Content filled task-by-task."""
import components as c
from i18n import L


def _stub():
    return c.pipeline(None) + c.lead(L("（本课内容建设中）", "(Lesson content coming soon)"))


LESSON_20 = (
    c.pipeline(None)
    + c.lead(L(
        "把前面每一站拼成一个<strong>可运行的本地 RAG 应用</strong>：加载 → 摄取/切块 → 建索引 → 持久化 → 检索 → 后处理 → "
        "合成 → 问答/多轮 → 评估。这一课就是“总装车间”。",
        "Assemble every stop into a <strong>runnable local RAG app</strong>: load → ingest/split → index → persist → "
        "retrieve → post-process → synthesize → Q&amp;A/chat → evaluate. This lesson is the final assembly line.",
    ))
    + c.analogy(L(
        "前面学的每个零件，现在装成一台完整的<strong>“知识问答机”</strong>——拧上电源就能跑。",
        "Every part you've learned now snaps together into a complete <strong>“knowledge answering machine”</strong> — "
        "plug it in and it runs.",
    ))
    + c.section(
        L("总装清单（每步回指对应课）", "Assembly checklist (each step links back to a lesson)"),
        c.compare_table(
            [L("步骤", "Step"), L("对应课", "Lesson")],
            [
                [L("加载 + 切块 + 抽取", "load + split + extract"), L("第 5 / 6 / 7 课", "Lessons 5 / 6 / 7")],
                [L("Embedding + 建索引 + 持久化", "embed + index + persist"), L("第 8 / 10 / 11 课", "Lessons 8 / 10 / 11")],
                [L("检索 + 后处理 + 合成", "retrieve + post-process + synthesize"), L("第 12 / 13 / 14 课", "Lessons 12 / 13 / 14")],
                [L("查询 / 多轮 / 评估", "query / chat / evaluate"), L("第 15 / 16 / 19 课", "Lessons 15 / 16 / 19")],
            ],
        ),
    )
    + c.source_ref("(综合 / integrates)", "VectorStoreIndex · IngestionPipeline · RetrieverQueryEngine · FaithfulnessEvaluator",
                   L("把全书组件拼到一起", "wires the whole guide's components together"))
    + c.code(
        "from llama_index.core import (\n"
        "    SimpleDirectoryReader, VectorStoreIndex, StorageContext,\n"
        "    load_index_from_storage, Settings, get_response_synthesizer,\n"
        ")\n"
        "from llama_index.core.node_parser import SentenceSplitter\n"
        "from llama_index.core.ingestion import IngestionPipeline\n"
        "from llama_index.core.postprocessor import SimilarityPostprocessor\n"
        "from llama_index.core.query_engine import RetrieverQueryEngine\n"
        "from llama_index.core.evaluation import FaithfulnessEvaluator\n"
        "from llama_index.llms.openai import OpenAI\n"
        "from llama_index.embeddings.openai import OpenAIEmbedding\n"
        "import os\n\n"
        "Settings.llm = OpenAI(model='gpt-4o-mini')\n"
        "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n\n"
        "PERSIST = './storage'\n"
        "if os.path.exists(PERSIST):                      # 已建过就秒加载\n"
        "    index = load_index_from_storage(StorageContext.from_defaults(persist_dir=PERSIST))\n"
        "else:                                            # 首次：摄取 -> 建索引 -> 落盘\n"
        "    docs = SimpleDirectoryReader('./data').load_data()\n"
        "    nodes = IngestionPipeline(transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=50)]).run(documents=docs)\n"
        "    index = VectorStoreIndex(nodes)\n"
        "    index.storage_context.persist(persist_dir=PERSIST)\n\n"
        "engine = RetrieverQueryEngine.from_args(\n"
        "    retriever=index.as_retriever(similarity_top_k=4),\n"
        "    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],\n"
        "    response_synthesizer=get_response_synthesizer(response_mode='compact'),\n"
        ")\n"
        "resp = engine.query('退款政策是什么？')\n"
        "print('答案:', resp)\n"
        "print('忠实度:', FaithfulnessEvaluator().evaluate_response(response=resp).passing)\n\n"
        "chat = index.as_chat_engine(chat_mode='condense_plus_context')\n"
        "print(chat.chat('那国际订单也一样吗？'))",
        caption=L("一个文件跑通完整 RAG（含持久化、后处理、评估、多轮）", "one file, full RAG: persistence, post-processing, eval, chat"),
    )
    + c.key_points([
        L("完整 RAG = 写入路径（建一次、落盘）+ 查询路径（反复问）。",
          "A full RAG = write path (build once, persist) + query path (ask repeatedly)."),
        L("每一站都是<strong>可替换</strong>组件：换库、换检索、换合成都不动主结构。",
          "Every stop is a <strong>swappable</strong> component: change store/retrieval/synthesis without touching the skeleton."),
        L("持久化 + 评估让它从 demo 走向<strong>可维护、可回归</strong>。",
          "Persistence + evaluation take it from demo to <strong>maintainable and regression-safe</strong>."),
    ])
    + c.design_highlight(L(
        "整条管道每一站都能独立替换，却共享统一接口——这正是 LlamaIndex 的核心思想：<strong>用可组合的标准件搭出你自己的 RAG</strong>。",
        "Every stop swaps independently yet shares one interface — that's LlamaIndex's core idea: <strong>compose your own "
        "RAG from standard, interchangeable parts</strong>.",
    ))
)
