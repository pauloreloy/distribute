from abc import ABC, abstractmethod


class Entity(ABC):


    def __init__(self, name: str):
        self.name = name

    
    @abstractmethod
    def set_data(self, data: str) -> None:
        pass
    

    @abstractmethod
    def run(self, data: str) -> str:
        pass