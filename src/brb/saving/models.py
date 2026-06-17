from abc import ABC, abstractmethod
from brb.llm.BaseLLM import BaseLLM
from dataclasses import dataclass, field
from datetime import datetime

class SavingModel(ABC):
    def __init__(self, message: str, lastcommands: list[str], executor: BaseLLM | None) -> None:
        self.lastcommands = lastcommands
        if executor: self.message = executor.createMessage(message, lastcommands)
        else: self.message = message

    @abstractmethod
    def converttodict(self) -> dict:
        pass

@dataclass
class Session:
    id: int
    folder: str
    message: str
    created_at: str
    commands: list[str] = field(default_factory=list)
    git_branch: str|None = None
    git_status: str|None = None