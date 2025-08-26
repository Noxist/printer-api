from pydantic import BaseModel
from typing import List

class PrintPayload(BaseModel):
    title: str = "TASKS"
    lines: List[str] = []
    cut: bool = True
    add_datetime: bool = True

class RawPayload(BaseModel):
    text: str
    add_datetime: bool = False
