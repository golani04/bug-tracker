from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    commenter: UUID
    reply_to: Optional[int]


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    updated_at: datetime
    created_at: datetime
