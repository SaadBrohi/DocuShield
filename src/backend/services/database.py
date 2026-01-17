import abc
import boto3
import json
import os
from datetime import datetime

class DatabaseProvider(abc.ABC):
    @abc.abstractmethod
    def save_result(self, doc_id: str, data: dict):
        pass

    @abc.abstractmethod
    def get_result(self, doc_id: str) -> dict:
        pass

class LocalDatabaseProvider(DatabaseProvider):
    def __init__(self, db_dir: str = "data/db"):
        self.db_dir = db_dir
        os.makedirs(self.db_dir, exist_ok=True)

    def save_result(self, doc_id: str, data: dict):
        path = os.path.join(self.db_dir, f"{doc_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def get_result(self, doc_id: str) -> dict:
        path = os.path.join(self.db_dir, f"{doc_id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

class DynamoDBProvider(DatabaseProvider):
    def __init__(self, table_name: str, region_name: str = "us-east-1"):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def save_result(self, doc_id: str, data: dict):
        # DynamoDB requires decimals instead of floats, handled by serializer usually
        # Adding timestamp
        item = {
            'document_id': doc_id,
            'timestamp': datetime.utcnow().isoformat(),
            **data
        }
        self.table.put_item(Item=item)

    def get_result(self, doc_id: str) -> dict:
        response = self.table.get_item(Key={'document_id': doc_id})
        return response.get('Item')
