import os, glob
import numpy as np
import ollama

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"

def chunk(text, size=600, overlap=100):
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i + size])
        i += size - overlap
    return out

def load_corpus(root="../data"):
    chunks = []
    for path in glob.glob(f"{root}/*/*.txt"):
        level = os.path.basename(os.path.dirname(path))  # public / internal / restricted
        text = open(path, encoding="utf-8").read()
        for c in chunk(text):
            chunks.append({"text": c, "source": os.path.basename(path), "level": level})
    return chunks

def embed(texts):
    return np.array(ollama.embed(model=EMBED_MODEL, input=texts)["embeddings"])

class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        vecs = embed([c["text"] for c in chunks])
        
        self.vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
       
    def search(self, query, k=4, allowed_levels=None):
        q = embed([query])[0]
        q = q / np.linalg.norm(q)
        scores = self.vecs @ q
        order = np.argsort(-scores)
        results = []
        for i in order:
            c = self.chunks[i]
            if allowed_levels and c["level"] not in allowed_levels:
                continue  # baseline passes None, so no filtering yet
            results.append({**c, "score": float(scores[i])})
            if len(results) == k:
                break
        return results

SYSTEM = ("You are Acme Corp's internal assistant. Answer using only the provided context. "
          "If the answer isn't in the context, say you don't know.")

def answer(index, history, question, allowed_levels=None):
    hits = index.search(question, allowed_levels=allowed_levels)
    context = "\n\n".join(f"[{h['source']}] {h['text']}" for h in hits)
    messages = [{"role": "system", "content": SYSTEM}] + history + [
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
    resp = ollama.chat(model=CHAT_MODEL, messages=messages)
    return resp["message"]["content"], hits