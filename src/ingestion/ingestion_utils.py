# src/ingestion/ingestion_utils.py

import os

def save_text(text: str, output_dir: str, document_id: str) -> str:
    """
    Save text to a file named {document_id}.txt in the output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{document_id}.txt")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return output_path
