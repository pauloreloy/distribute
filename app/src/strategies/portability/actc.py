import re
from typing                                     import Dict, Any
from src.strategies.portability.portability     import Portability
from src.utils.utils                            import Utils
from src.decorators.actc                        import count_processing
from src.decorators.exceptions                  import exception_decorator


class ACTC(Portability):


    def __init__(self):
        super().__init__()
        self.total_run = 0


    def set_data(self, data: Dict[dict, Any]) -> None:
        self.actc_data = data


    @exception_decorator
    def process_ret(self, context, actc_data):
        context.set_strategy("ACTC_RET")
        return context.run(context, self.aws_client, actc_data)


    @exception_decorator
    def process_actc(self, context, actc_data):
        print(f"NUPortlddCTC: {actc_data.get('actc', {}).get('NUPortlddCTC')}, actc_type: {actc_data['actc_type']}, group: {actc_data['group']}")
        return True

    
    def run(self, context: object, aws_client: object, actc_data: Dict[dict, Any]) -> bool:
        self.total_run += 1
        self.aws_client = aws_client
        actc_type       = actc_data.get("actc_type")
        if re.match(r"^ACTC.*(RET|4)$", actc_type):
            return self.process_ret(context, actc_data)
        return self.process_actc(context, actc_data)