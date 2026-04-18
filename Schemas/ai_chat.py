from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class AIConsultRequest(BaseModel):
    user_id: Optional[int] = None
    messages: List[ChatMessage] = Field(min_length=1)
    model: Optional[str] = None
    temperature: float = Field(default=0.3, ge=0, le=2)


class AIConsultResponse(BaseModel):
    model: str
    answer: str
    provider: str = "openrouter"
