from abc import ABC, abstractmethod
from brb.llm.BaseLLM import AgentLLM

class SavingModel(ABC):
    def __init__(self, message: str, lastcommands: list[str], executor: AgentLLM | None) -> None:
        self.lastcommands = lastcommands
        if executor: self.message = executor.createMessage(message, lastcommands)
        else: self.message = message

    @abstractmethod
    def converttodict(self) -> dict:
        pass