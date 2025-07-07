from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.sql import func
from app.database import Base

class SupportTicket(Base):
    """support ticket model"""

    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    
    subject = Column(String(50), nullable=True)
    body = Column(Text, nullable=False)
    original_queue = Column(String(50), nullable=True) 
    original_priority = Column(String(50), nullable=True) 
    language = Column(String(10), default="en") 

    
    category = Column(String(50), nullable=True) 
    confidence_score = Column(Float, nullable=True) 
    summary = Column(Text, nullable=True) 

    tag_1 = Column(String(100), nullable=True)
    tag_2 = Column(String(100), nullable=True)
    tag_3 = Column(String(100), nullable=True)
    tag_4 = Column(String(100), nullable=True)
    tag_5 = Column(String(100), nullable=True)
    tag_6 = Column(String(100), nullable=True)
    tag_7 = Column(String(100), nullable=True)
    tag_8 = Column(String(100), nullable=True)

    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_processed = Column(Boolean, default=False)


