from pydantic import BaseModel
from typing import List, Optional


class UploadIn(BaseModel):
    doc_id: Optional[str]
    text: str
    metadata: Optional[dict] = None


class UploadOut(BaseModel):
    status: str
    doc_id: str


class ChatIn(BaseModel):
    query: str
    top_k: Optional[int] = None


class ChatOut(BaseModel):
    answer: str
    source_chunks: List[dict]