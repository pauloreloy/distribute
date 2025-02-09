
from typing import Any
from src.strategies.entities.nuclea         import Nuclea
from src.strategies.portability.actc        import ACTC
from src.strategies.portability.actc_ret    import ACTC_RET


class Context:


    strategies = {
        "NUCLEA":       Nuclea,
        "ACTC":         ACTC,
        "ACTC_RET":     ACTC_RET,
    }


    def __init__(self, strategy: Any) -> None:
        self.strategy = self.strategies[strategy]()


    def set_strategy(self, strategy: Any) -> None:
        if(self.strategy != self.strategies[strategy]):
            self.strategy = self.strategies[strategy]()


    def run(self, context: object, aws_client: object, data: Any) -> Any:
        return self.strategy.run(context, aws_client, data)