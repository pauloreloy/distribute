
from typing import Any  
from src.strategies.entities.nuclea import Nuclea


class Context:


    strategies = {
        "nuclea":   Nuclea
    }


    def __init__(self, strategy: Any) -> None:
        self.strategy = self.strategies[strategy]()


    def set_strategy(self, strategy: Any) -> None:
        if(self.strategy != self.strategies[strategy]):
            self.strategy = self.strategies[strategy]()


    def set_data(self, data: Any) -> None:
        self.strategy.set_data(data)
        

    def run(self, aws_client: object) -> Any:
        return self.strategy.run(aws_client)