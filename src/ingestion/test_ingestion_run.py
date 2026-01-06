# src/ingestion/test_ingestion_run.py

import os
from pdf_parser import parse_pdf
from docx_parser import parse_docx
from pptx_parser import parse_pptx

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

for file_name in os.listdir(RAW_DIR):
    file_path = os.path.join(RAW_DIR, file_name)
    document_id = os.path.splitext(file_name)[0]  # Use file name as ID
    
    if file_name.endswith(".pdf"):
        output = parse_pdf(file_path, PROCESSED_DIR, document_id)
    elif file_name.endswith(".docx"):
        output = parse_docx(file_path, PROCESSED_DIR, document_id)
    elif file_name.endswith(".pptx"):
        output = parse_pptx(file_path, PROCESSED_DIR, document_id)
    else:
        continue
    
    print(f"Processed {file_name} → {output}")
