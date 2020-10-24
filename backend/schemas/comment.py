from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    text: str
    commenter: UUID
    reply_to: Optional[int] = Field(None, description="Replying to the previous comment")


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
