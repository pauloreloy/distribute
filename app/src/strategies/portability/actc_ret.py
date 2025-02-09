from typing                                     import Dict, Any
from src.strategies.portability.portability     import Portability


class ACTC_RET(Portability):


    def __init__(self):
        super().__init__()

    
    def set_data(self, data: Dict[dict, Any]) -> None:
        self.actc_data = data

    
    def run(self, context: object, aws_client: object, actc_data: Dict[dict, Any]) -> bool:
        self.aws_client = aws_client
        print(f"NUPortlddCTC: {actc_data.get('actc', {}).get('NUPortlddCTC')}, actc_type: {actc_data['actc_type']}, group: {actc_data['group']}")
        return True