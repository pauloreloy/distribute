from abc import ABC, abstractmethod
from typing import Dict, Any


class Portability(ABC):

    def __init__(self):
        super().__init__()


    @abstractmethod
    def set_data(self, data: Dict[dict, Any]) -> None:
        pass
