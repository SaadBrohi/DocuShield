import os
import uuid
import shutil
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.backend.services.llm_service import LLMService

# Providers
from src.backend.services.storage import LocalStorageProvider, S3StorageProvider
from src.backend.services.ocr import LocalOCRProvider, TextractOCRProvider
from src.backend.services.database import LocalDatabaseProvider, DynamoDBProvider
from src.ai_models import embeddings
from src.ai_models.embeddings import embeddings_dir, model

class PipelineService:
    def __init__(self):
        self.llm_service = LLMService()
        
        # Load Providers based on Env
        self.use_aws = os.getenv("USE_AWS", "false").lower() == "true"
        
        if self.use_aws:
            self.bucket_name = os.getenv("S3_BUCKET_NAME", "docushield-docs")
            self.storage = S3StorageProvider(bucket_name=self.bucket_name, region_name=os.getenv("AWS_REGION", "us-east-1"))
            self.ocr = TextractOCRProvider(region_name=os.getenv("AWS_REGION", "us-east-1"))
            self.db = DynamoDBProvider(table_name=os.getenv("DYNAMODB_TABLE", "DocuShieldAudit"))
        else:
            self.storage = LocalStorageProvider()
            self.ocr = LocalOCRProvider()
            self.db = LocalDatabaseProvider()

    def process_upload(self, file_content: bytes, filename: str) -> str:
        doc_id = str(uuid.uuid4())
        
        # 1. Save File using Provider
        file_path = self.storage.save_file(file_content, filename)

        # 2. OCR / Text Extraction using Provider
        # Note: Local OCR might need the local path. S3 provider returns s3:// uri.
        # Our providers handle this logic internally now.
        text = self.ocr.extract_text(file_path, doc_id)
        
        # Save text locally for embeddings (simplification for MVP)
        # In a real cloud app, we'd save text to S3 too or pass text directly to embedding service
        temp_text_path = os.path.join("data/processed", f"{doc_id}.txt")
        with open(temp_text_path, "w", encoding="utf-8") as f:
            f.write(text)

        # 3. Embeddings (Vector Store)
        sentences, emb = embeddings.embed_text_file(temp_text_path)
        if self.use_aws:
            embeddings.save_embeddings_s3(self.bucket_name, doc_id, sentences, emb, region_name=os.getenv("AWS_REGION", "us-east-1"))
        else:
            embeddings.save_embeddings(doc_id, sentences, emb)
        
        return doc_id

    def get_document_text(self, doc_id: str) -> str:
        # Simplification: Try reading from local processed first
        path = os.path.join("data/processed", f"{doc_id}.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def analyze_document(self, doc_id: str):
        # Check DB first? Or re-run? Let's check DB.
        cached_result = self.db.get_result(doc_id)
        if cached_result:
            return cached_result

        text = self.get_document_text(doc_id)
        if not text:
            raise FileNotFoundError("Document text not found")
        
        result = self.llm_service.analyze_risk(text)
        
        # Save validation result
        self.db.save_result(doc_id, result)
        
        return result

    def query_document(self, doc_id: str, query: str):
        # 1. Find relevant chunks
        data = None
        if self.use_aws:
            data = embeddings.load_embeddings_s3(self.bucket_name, doc_id, region_name=os.getenv("AWS_REGION", "us-east-1"))
            if not data:
                return "Processing not complete or embeddings missing from S3."
        else:
            emb_path = os.path.join(embeddings_dir, f"{doc_id}.json")
            if not os.path.exists(emb_path):
                 return "Processing not complete or embeddings missing."

            with open(emb_path, "r", encoding="utf-8") as f:
                data = json.load(f) # List of {sentence, embedding}
            
        # Compute query embedding
        query_embedding = model.encode([query], convert_to_numpy=True)[0]
        
        # Extract vectors
        doc_embeddings = np.array([item['embedding'] for item in data])
        sentences = [item['sentence'] for item in data]
        
        if len(doc_embeddings) == 0:
             return "Document is empty."

        # Compute cosine similarity
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        
        # Get top k
        top_k_indices = similarities.argsort()[-5:][::-1]
        top_chunks = [sentences[i] for i in top_k_indices]
        
        # 2. Call LLM
        return self.llm_service.chat_with_document(top_chunks, query)

