import os
import shutil
import abc
from typing import Optional
import boto3
from botocore.exceptions import NoCredentialsError

class StorageProvider(abc.ABC):
    @abc.abstractmethod
    def save_file(self, file_content: bytes, filename: str) -> str:
        """Save file and return a path or identifier."""
        pass

    @abc.abstractmethod
    def get_file(self, file_path: str) -> bytes:
        """Retrieve file content."""
        pass

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_dir: str = "data/raw"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_file(self, file_content: bytes, filename: str) -> str:
        path = os.path.join(self.base_dir, filename)
        with open(path, "wb") as f:
            f.write(file_content)
        return path

    def get_file(self, file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            return f.read()

class S3StorageProvider(StorageProvider):
    def __init__(self, bucket_name: str, region_name: str = "us-east-1"):
        self.bucket = bucket_name
        self.s3 = boto3.client('s3', region_name=region_name)

    def save_file(self, file_content: bytes, filename: str) -> str:
        try:
            self.s3.put_object(Bucket=self.bucket, Key=filename, Body=file_content)
            return f"s3://{self.bucket}/{filename}"
        except NoCredentialsError:
            print("AWS Credentials not found. File not saved to S3.")
            raise

    def get_file(self, file_path: str) -> bytes:
        # file_path is expected to be s3://bucket/key or just key if we handle parsing
        key = file_path.replace(f"s3://{self.bucket}/", "")
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        return response['Body'].read()
