import boto3
from typing import Dict, Any   


class AWS:


    def __init__(self):
        self.client = boto3.client('s3')


    def get_object(self, bucket: str, key: str) -> Dict[str, Any]:
        with open(key) as event_file:
            return event_file.read()
        