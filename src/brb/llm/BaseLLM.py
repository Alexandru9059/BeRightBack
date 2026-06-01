from abc import ABC, abstractmethod

__PROMPT = """
    Considering the last commands
"""

class BaseLLM(ABC):
    def __init__(self, option: bool, model: str):
        pass

    @abstractmethod
    def createMessage(self, message, lastcommands: list[str]) -> str:
        pass

class AgentLLM(BaseLLM):
    def createMessage(self, message, lastcommands: list[str]) -> str:
        pass