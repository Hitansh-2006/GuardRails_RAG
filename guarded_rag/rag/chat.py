from rag.core import load_corpus, Index, answer

index = Index(load_corpus())
history = []
while True:
    q = input("you> ")
    if q.strip() in {"exit", "quit"}:
        break
    a, hits = answer(index, history, q)
    print("bot>", a, "\n   sources:", [h["source"] for h in hits])
    history += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]