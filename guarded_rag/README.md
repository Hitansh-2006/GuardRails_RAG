# Guarded RAG

A retrieval-augmented generation project with input, retrieval, and output guard
scaffolding.

## Project layout

- `rag/`: baseline retrieval and generation code
- `guards/`: input, retrieval, and output guard modules
- `data/`: public, internal, and restricted sample corpora
- `eval/`: attack and benign evaluation cases
- `tests/`: guard unit tests

The guard modules are scaffold files and can be implemented incrementally.
