from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class NewsBase(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    content: str = Field(min_length=1)


class NewsCreate(NewsBase):
    pass


class NewsOut(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    author_name: Optional[str] = None
    created_at: datetime
