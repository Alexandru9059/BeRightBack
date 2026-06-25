from abc import ABC, abstractmethod
from brb.llm.BaseLLM import BaseLLM
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Session:
    folder: str
    message: str
    commands: list[str] = field(default_factory=list)
    git_branch: str|None = None
    git_status: str|None = None
    id: int|None = None
    created_at: str|None = None