# src/ingestion/docx_parser.py

from docx import Document
from ingestion_utils import save_text

def parse_docx(file_path: str, output_dir: str, document_id: str) -> str:
    """
    Extract text from a DOCX file and save it.
    """
    doc = Document(file_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    
    output_path = save_text(full_text, output_dir, document_id)
    return output_path
