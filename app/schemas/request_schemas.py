from pydantic import BaseModel, Field, validator
from typing import Optional

class SupportRequestCreate(BaseModel):
    """support request model"""

    text: Optional[str] = Field(None, min_length=1, max_length=10000)

    subject: Optional[str] = Field(None, max_length=10000)
    body: Optional[str] = Field(None, min_length=1, max_length=10000)

    @validator("text", "subject", "body")
    def validate_text_length(cls, v, values):
        """check text length"""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Text must be at least 10 characters long")
        # TODO: add content filtering
        return v
    
    @validator("body", always=True)
    def validate_content(cls, v, values):
        """make sure we have some content"""
        if not values.get("text") and not v:
            raise ValueError("Either 'text' or 'body' must be provided")
        return v
    
class SupportRequestFilter(BaseModel):
    category: Optional[str] = Field(None, pattern=r"^(technical|billing|general)$")
    limit: int = Field(default=10, ge=1, le=500)
    offset: int = Field(default=0, ge=0)
    sort: Optional[str] = Field(None, max_length=50)
    order: Optional[str] = Field(None, max_length=50)
    search: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=50)
    created_at: Optional[str] = Field(None, max_length=50)
    updated_at: Optional[str] = Field(None, max_length=50)
    is_processed: Optional[bool] = Field(None)