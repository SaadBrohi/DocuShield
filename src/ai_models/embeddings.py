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

def save_embeddings_s3(bucket_name, doc_id, sentences, embeddings, region_name="us-east-1"):
    """Save embeddings to S3 as a JSON file."""
    try:
        import boto3
        s3 = boto3.client('s3', region_name=region_name)
        
        data = [{"sentence": s, "embedding": e.tolist()} for s, e in zip(sentences, embeddings)]
        json_content = json.dumps(data)
        
        # Save to S3 under an 'embeddings/' prefix or similar
        key = f"embeddings/{doc_id}.json"
        s3.put_object(Bucket=bucket_name, Key=key, Body=json_content)
        print(f"Saved embeddings to s3://{bucket_name}/{key}")
    except ImportError:
        print("boto3 not installed, cannot save to S3")
    except Exception as e:
        print(f"Error saving embeddings to S3: {e}")
        raise

def load_embeddings_s3(bucket_name, doc_id, region_name="us-east-1"):
    """Load embeddings from S3."""
    try:
        import boto3
        s3 = boto3.client('s3', region_name=region_name)
        
        key = f"embeddings/{doc_id}.json"
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Error loading embeddings from S3: {e}")
        return None
