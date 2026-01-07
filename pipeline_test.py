# pipeline_test.py
import os
import uuid
import numpy as np
import nltk

# -----------------------------
# Download necessary NLTK resources
# -----------------------------
nltk.download('punkt')       # sentence tokenizer
nltk.download('stopwords')   # stopwords
nltk.download('wordnet')     # lemmatizer
nltk.download('omw-1.4')     # wordnet auxiliary data

# -----------------------------
# Imports
# -----------------------------
from src.ingestion import pdf_parser, docx_parser, pptx_parser
from src.preprocessing import text_cleaner, tokenizer, preprocessing_utils
from src.ai_models import embeddings

# -----------------------------
# Paths
# -----------------------------
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
EMBEDDINGS_DIR = "data/embeddings"

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# -----------------------------
# Ingestion
# -----------------------------
def test_ingestion():
    print("=== Testing Data Ingestion ===")
    all_docs = []

    for fname in os.listdir(RAW_DATA_DIR):
        fpath = os.path.join(RAW_DATA_DIR, fname)
        doc_id = str(uuid.uuid4())

        # Select parser
        if fname.lower().endswith(".pdf"):
            out_path = pdf_parser.parse_pdf(fpath, PROCESSED_DATA_DIR, doc_id)
        elif fname.lower().endswith(".docx"):
            out_path = docx_parser.parse_docx(fpath, PROCESSED_DATA_DIR, doc_id)
        elif fname.lower().endswith(".pptx"):
            out_path = pptx_parser.parse_pptx(fpath, PROCESSED_DATA_DIR, doc_id)
        else:
            print(f"Skipping unsupported file: {fname}")
            continue

        # Read text from saved file
        with open(out_path, "r", encoding="utf-8") as f:
            text = f.read()

        print(f"Parsed {fname} -> doc_id {doc_id}, length: {len(text)} characters")
        all_docs.append((doc_id, fname, text))

    return all_docs

# -----------------------------
# Preprocessing
# -----------------------------
def test_preprocessing(docs):
    print("\n=== Testing Preprocessing ===")
    processed_docs = []

    # Instantiate processors
    cleaner = text_cleaner.TextCleaner(remove_numbers=True, lower_case=True)
    sent_tokenizer = tokenizer.Tokenizer(lowercase=True)
    prep_utils = preprocessing_utils.PreprocessingUtils(language="english")

    for doc_id, fname, text in docs:
        # Clean text
        cleaned = cleaner.clean_text(text)

        # Sentence-level tokenization
        sentence_tokens = sent_tokenizer.sentence_tokenize(cleaned)

        # Word-level tokenization + stopword removal + lemmatization
        word_tokens = prep_utils.preprocess_text(cleaned)

        processed_docs.append((doc_id, fname, cleaned, sentence_tokens, word_tokens))

        # Save cleaned text
        out_path = os.path.join(PROCESSED_DATA_DIR, f"{doc_id}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"{fname} (doc_id {doc_id}) -> {len(sentence_tokens)} sentences, {len(word_tokens)} words after preprocessing")

    return processed_docs

# -----------------------------
# Embeddings
# -----------------------------
def test_embeddings(processed_docs):
    print("\n=== Testing Embeddings ===")
    for doc_id, fname, cleaned, sentence_tokens, word_tokens in processed_docs:
        # Use embeddings module functions
        file_path = os.path.join(PROCESSED_DATA_DIR, f"{doc_id}.txt")
        sentences, emb = embeddings.embed_text_file(file_path)
        embeddings.save_embeddings(doc_id, sentences, emb)
        print(f"Saved embeddings for {fname} (doc_id {doc_id}), sentences: {len(sentences)}, embedding shape: {emb.shape}")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    docs = test_ingestion()
    if not docs:
        print("No documents found in raw data folder!")
        exit(1)

    processed_docs = test_preprocessing(docs)
    test_embeddings(processed_docs)
    print("\n=== Pipeline Test Completed Successfully ===")
