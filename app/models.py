from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class MediaItem(BaseModel):
    url: str
    type: str  # e.g., 'photo', 'video'

class CreateMemoryRequest(BaseModel):
    user_id: str
    title: str
    date: date
    context: Optional[str] = None
    media: List[MediaItem]
    people: List[str]
    location: str
    event: str

class MemoryResponse(BaseModel):
    id: str
    title: str
    date: date
    context: Optional[str] = None

    class Config:
        orm_mode = True

class BasicSearchResponse(BaseModel):
    memories: List[MemoryResponse]

class NaturalLanguageSearchRequest(BaseModel):
    query: str

class NaturalLanguageSearchResponse(BaseModel):
    answer: str

class Memory(BaseModel):
    text: str