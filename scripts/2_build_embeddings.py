import os
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# -------------------------------
# Paths
# -------------------------------
PROJECT_ROOT = r"C:\Users\Hp\Desktop\Cybersecurity_RAG"
CLEANED_CHUNKS_PATH = os.path.join(PROJECT_ROOT, "data", "cleaned", "chunks.json")
INDEX_DIR = os.path.join(PROJECT_ROOT, "indexes")

CHUNKS_PKL_PATH = os.path.join(INDEX_DIR, "chunks.pkl")
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "index.faiss")
META_PATH = os.path.join(INDEX_DIR, "meta.json")

os.makedirs(INDEX_DIR, exist_ok=True)

# -------------------------------
# Load chunks
# -------------------------------
if not os.path.exists(CLEANED_CHUNKS_PATH):
    raise FileNotFoundError(f"Chunks file not found: {CLEANED_CHUNKS_PATH}")

with open(CLEANED_CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Skip empty texts
chunks = [c for c in chunks if c["text"].strip()]
texts = [c["text"] for c in chunks]

if not texts:
    raise ValueError("❌ No valid text found in chunks.json. Check your preprocessing step.")

# -------------------------------
# Build embeddings + FAISS index
# -------------------------------
model_name = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model_name)

print("🔢 Generating embeddings...")
embeddings = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # Inner Product = cosine similarity if embeddings are normalized
index.add(np.array(embeddings, dtype="float32"))

# -------------------------------
# Save index + metadata
# -------------------------------
faiss.write_index(index, FAISS_INDEX_PATH)

with open(CHUNKS_PKL_PATH, "wb") as f:
    pickle.dump(chunks, f)

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump({"model": model_name, "dim": dim, "count": len(chunks)}, f, indent=2)

print(f"✅ FAISS index saved to {FAISS_INDEX_PATH}")
print(f"✅ Chunks metadata saved to {CHUNKS_PKL_PATH}")
print(f"✅ Model info saved to {META_PATH}")
