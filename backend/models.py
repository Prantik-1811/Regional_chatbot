from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    region: Optional[str] = None  # Optional region filter: "HK", "JP", "NYC", or None for all

class Source(BaseModel):
    title: str
    url: str
    region: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
