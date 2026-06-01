from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def createMessage(self, message, lastcommands: list[str]) -> str:
        pass