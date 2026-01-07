import os

def save_text(text: str, output_dir: str, document_id: str) -> str:
    """
    Safely save text to a file with the given document_id.
    Ensures the file is closed properly before returning the path.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{document_id}.txt")

    # Use 'with' to ensure file is closed immediately
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path
