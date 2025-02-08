import boto3
from typing                 import Optional
from src.config.params      import local


class AWS:


    def __init__(self):
        self.s3_client = boto3.client('s3')


    def get_s3_object(self, bucket: str, key: str) -> Optional[str]:
        if local:
            with open(key, "r") as file:
                return file.read()
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Error: {e}")
        