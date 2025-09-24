from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class GeminiBaseResponse(BaseModel):
    model: str
    date: datetime
    error: Optional[str]

class TestAgentResponse(GeminiBaseResponse):
    tests: list[str]

class DeveloperAgentResponse(GeminiBaseResponse):
    html: str
    css: str
    js: str