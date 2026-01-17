import os
import sys

sys.path.append(os.getcwd())

from src.ingestion.pdf_parser import parse_pdf

raw_dir = "data/raw"
files = [f for f in os.listdir(raw_dir) if f.endswith(".pdf")]

if not files:
    print("No PDF files in data/raw to test.")
    sys.exit(1)

test_file = os.path.join(raw_dir, files[0])
print(f"Testing parsing on: {test_file}")

try:
    # Use a dummy output dir or ensure data/processed exists
    output_dir = "data/processed"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    doc_id = "test_doc_parsing"
    out_path = parse_pdf(test_file, output_dir, doc_id)
    print(f"Success! Output saved to: {out_path}")
    
    with open(out_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"Content preview: {content[:100]}...")
except Exception as e:
    print(f"ERROR parsing PDF: {e}")
    import traceback
    traceback.print_exc()
