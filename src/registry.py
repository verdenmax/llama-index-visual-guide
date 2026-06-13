"""Single source of truth: ordered filename -> lesson HTML content.

Both build.py (site) and build_print.py (PDF source) import this so the lesson
set stays in sync with shell.PAGES.
"""
import part1
import part2
import part3
import part4
import part5
import glossary

CONTENT = {
    "01-what-is-llamaindex.html": part1.LESSON_01,
    "02-architecture.html": part1.LESSON_02,
    "03-rag-lifecycle.html": part1.LESSON_03,
    "04-documents-nodes.html": part2.LESSON_04,
    "05-readers.html": part2.LESSON_05,
    "06-node-parsers.html": part2.LESSON_06,
    "07-metadata-extractors.html": part2.LESSON_07,
    "08-embeddings.html": part2.LESSON_08,
    "09-vector-stores.html": part2.LESSON_09,
    "10-index-abstraction.html": part2.LESSON_10,
    "11-ingestion-storage.html": part2.LESSON_11,
    "12-retrievers.html": part3.LESSON_12,
    "13-postprocessors.html": part3.LESSON_13,
    "14-response-synthesizers.html": part3.LESSON_14,
    "15-query-engine.html": part3.LESSON_15,
    "16-chat-engine.html": part3.LESSON_16,
    "17-settings-prompts.html": part4.LESSON_17,
    "18-advanced-retrieval.html": part4.LESSON_18,
    "19-evaluation.html": part4.LESSON_19,
    "20-capstone.html": part5.LESSON_20,
    "21-glossary.html": glossary.LESSON_21,
}
