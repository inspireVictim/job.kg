from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    original_filename: str
    size_bytes: int
    uploaded_by: int
    uploader_name: Optional[str] = None
    uploaded_at: datetime
