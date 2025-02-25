import json
from typing                     import Dict, Any
from src.decorators.exceptions  import exception_decorator
from src.classes.business       import Business
from src.adapter.aws.aws        import AWS


aws = AWS()


@exception_decorator
def validate_event(event_record: Dict[dict, Any]) -> Any:
    if event_record.get("eventSource") == 'aws:s3':
        return Business(aws).process_s3_event(event_record)


def lambda_handler(event, context):
    if event.get("Records"):
        for event_record in event['Records']:
            validate_event(event_record)


if __name__ == "__main__":
    #caminho_json = "feriados.json"
    
    with open('event.json') as event_file:
        event = json.loads(event_file.read())
        lambda_handler(event, None)
