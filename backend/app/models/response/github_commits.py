from pydantic import BaseModel, Json
from datetime import datetime
from typing import List


class CommitResponse(BaseModel):
    id: int
    project_id: int
    github_url: str
    commit_hash: str
    commit_author: str
    commit_message: str
    commit_date: datetime
    commit_summary: Json  # Assuming your commit summary is a list of strings
    commit_avatar_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = (
            True  # This tells Pydantic to convert SQLAlchemy models to Pydantic models
        )
