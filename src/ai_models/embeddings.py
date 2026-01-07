# src/ai_models/embeddings.py

from sentence_transformers import SentenceTransformer
import os
import json

# Load the model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Paths
processed_dir = os.path.join("data", "processed")
embeddings_dir = os.path.join("data", "embeddings")
os.makedirs(embeddings_dir, exist_ok=True)

def embed_text_file(file_path):
    """Read a text file, generate embeddings for each sentence, and return."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Split into sentences if needed (or embed entire text as one vector)
    sentences = [line.strip() for line in text.split("\n") if line.strip()]
    embeddings = model.encode(sentences, convert_to_numpy=True, show_progress_bar=True)
    return sentences, embeddings

def save_embeddings(file_name, sentences, embeddings):
    """Save embeddings as a JSON file (can also use npy or pickle)."""
    out_path = os.path.join(embeddings_dir, f"{file_name}.json")
    data = [{"sentence": s, "embedding": e.tolist()} for s, e in zip(sentences, embeddings)]
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved embeddings to {out_path}")

def process_all_files():
    for file_name in os.listdir(processed_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(processed_dir, file_name)
            sentences, embeddings = embed_text_file(file_path)
            save_embeddings(os.path.splitext(file_name)[0], sentences, embeddings)

if __name__ == "__main__":
    process_all_files()
