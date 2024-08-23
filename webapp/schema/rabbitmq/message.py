from typing import Any

from pydantic import BaseModel


class BaseMessage(BaseModel):
    author: str
    message: dict[Any, Any]
