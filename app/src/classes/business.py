
from typing                     import Dict, Any
from src.decorators.strategy    import make_strategy


class Business:


    def __init__(self, aws_client: object = None):
        self.aws_client = aws_client


    def make_strategy(self, strategy: str):
        @make_strategy(strategy)
        def _make_strategy():
            return strategy
        return _make_strategy()


    def identify_entity(self, data: str, object_key: str) -> Any:
        if("O7DOC" in data and "ACTC" in data):
            return self.create_strategy("NUCLEA", data)


    def process_s3_event(self, event_record: Dict[dict, Any]) -> Any:
        bucket_name = event_record["s3"]["bucket"]["name"]
        object_key  = event_record["s3"]["object"]["key"]
        if object_key and bucket_name:
            data = self.aws_client.get_s3_object(bucket_name, object_key)
            if data:
                return self.identify_entity(data, object_key)
        return None


    def create_strategy(self, strategy: str, data: Any) -> Any:
        context = self.make_strategy(strategy)
        if context:
            return context.run(context, self.aws_client, data)
