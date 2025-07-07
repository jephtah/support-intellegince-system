from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SupportTicketResponse(BaseModel):
    """ticket response"""
    id: int
    subject: Optional[str] = None
    body: str
    category: Optional[str] = None
    confidence_score: Optional[float] = None
    summary: Optional[str] = None
    original_queue: Optional[str] = None
    original_priority: Optional[str] = None
    language: str
    is_processed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SupportTicketList(BaseModel):
    """paginated ticket list"""
    total: int
    limit: int
    offset: int
    tickets: List[SupportTicketResponse]

class CategoryStats(BaseModel):
    """stats response"""
    technical: int
    billing: int
    general: int
    total: int
    unclassified: int

class ErrorResponse(BaseModel):
    """error response"""
    detail: str
    status_code: Optional[str] = None

