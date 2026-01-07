# src/ingestion/pdf_parser.py

import fitz  # PyMuPDF
from .ingestion_utils import save_text

def parse_pdf(file_path: str, output_dir: str, document_id: str) -> str:
    """
    Extract text from a PDF and save it to a .txt file.
    
    Args:
        file_path (str): Path to the PDF file
        output_dir (str): Directory to save processed text
        document_id (str): Unique document ID
        
    Returns:
        str: Path to the saved text file
    """
    doc = fitz.open(file_path)
    full_text = ""
    
    for page in doc:
        text = page.get_text()
        full_text += text + "\n"
    
    doc.close()
    
    # Save extracted text
    output_path = save_text(full_text, output_dir, document_id)
    return output_path
