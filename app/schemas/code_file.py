from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.user import User

class CodeFileBase(BaseModel):
    name: str
    language: str
    content: str = ""

class CodeFileCreate(CodeFileBase):
    pass

class CodeFileUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    language: Optional[str] = None

class CollaboratorInfo(BaseModel):
    user: User
    role: str

class CodeFile(CodeFileBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: User
    collaborators: List[CollaboratorInfo] = []

    class Config:
        from_attributes = True 