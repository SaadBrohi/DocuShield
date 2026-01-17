import abc
import os
import boto3
import time
from src.ingestion import pdf_parser, docx_parser

class OCRProvider(abc.ABC):
    @abc.abstractmethod
    def extract_text(self, file_path: str, doc_id: str) -> str:
        """Extract text from file and return the text content."""
        pass

class LocalOCRProvider(OCRProvider):
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir

    def extract_text(self, file_path: str, doc_id: str) -> str:
        # file_path is local path
        if file_path.endswith(".pdf"):
            out_path = pdf_parser.parse_pdf(file_path, self.output_dir, doc_id)
        elif file_path.endswith(".docx"):
            out_path = docx_parser.parse_docx(file_path, self.output_dir, doc_id)
        else:
            raise ValueError("Unsupported file type")
        
        with open(out_path, "r", encoding="utf-8") as f:
            return f.read()

class TextractOCRProvider(OCRProvider):
    def __init__(self, region_name: str = "us-east-1"):
        self.textract = boto3.client('textract', region_name=region_name)

    def extract_text(self, file_path: str, doc_id: str) -> str:
        # For Textract, file_path usually must be an S3 object or bytes.
        # Assuming file_path here is "s3://bucket/key"
        if not file_path.startswith("s3://"):
             raise ValueError("Textract requires S3 path")

        bucket = file_path.split("/")[2]
        key = "/".join(file_path.split("/")[3:])

        response = self.textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
        )
        job_id = response['JobId']
        
        # Poll for completion
        while True:
            response = self.textract.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            if status in ['SUCCEEDED', 'FAILED']:
                break
            time.sleep(1)

        if status == 'SUCCEEDED':
            text = ""
            for item in response['Blocks']:
                if item['BlockType'] == 'LINE':
                    text += item['Text'] + "\n"
            return text
        else:
            raise Exception("Textract job failed")
