from typing import Optional
from sqlmodel import SQLModel

class ItemRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None

class ItemCreate(SQLModel):
    name: str
    description: Optional[str] = None
