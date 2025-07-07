from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.support_ticket import SupportTicket
from app.schemas.request_schemas import SupportRequestCreate, SupportRequestFilter
from app.schemas.response_schemas import CategoryStats
from app.services.ai_service import AIService
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TicketService:
    """ticket service - handles crud and ai stuff"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def create_ticket(self, db: Session, request: SupportRequestCreate) -> SupportTicket:
        """create ticket and run ai on it"""
        
        # get text content
        if request.text:
            body = request.text
            subject = None
        else:
            body = request.body
            subject = request.subject  # might be None
        
        # create ticket
        ticket = SupportTicket(
            subject=subject,
            body=body,
            is_processed=False
        )
        
        # save to db first to get id
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        
        # run ai
        await self._process_ticket_ai(db, ticket)
        
        return ticket
    
    async def _process_ticket_ai(self, db: Session, ticket: SupportTicket):
        """run ai on ticket"""
        try:
            # Get AI classification results
            ai_result = await self.ai_service.classify_and_summarize(
                ticket.body, 
                ticket.subject
            )
            
            # update ticket
            ticket.category = ai_result.get("category")
            ticket.confidence_score = ai_result.get("confidence")
            ticket.summary = ai_result.get("summary")
            ticket.is_processed = True
            
            db.commit()
            logger.info(f"processed ticket {ticket.id} - {ticket.category}")
            
        except Exception as e:
            # log error but don't fail
            logger.error(f"ai failed for ticket {ticket.id}: {str(e)}")
            ticket.is_processed = False
            # TODO: add retry logic
            db.commit()
    
    def get_ticket(self, db: Session, ticket_id: int) -> Optional[SupportTicket]:
        """get ticket by id"""
        return db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    
    def get_tickets(self, db: Session, filters: SupportRequestFilter) -> Tuple[List[SupportTicket], int]:
        """get tickets with filters and pagination"""
        query = db.query(SupportTicket)
        
        # filter by category
        if filters.category:
            query = query.filter(SupportTicket.category == filters.category)
        
        # get total count
        total = query.count()
        
        # pagination - TODO: optimize for large datasets
        tickets = query.order_by(SupportTicket.created_at.desc())\
                      .offset(filters.offset)\
                      .limit(filters.limit)\
                      .all()
        
        return tickets, total
    
    def get_category_stats(self, db: Session, days: int = 7) -> CategoryStats:
        """get stats for last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # get category counts
        stats = db.query(
            SupportTicket.category,
            func.count(SupportTicket.id).label('count')
        ).filter(
            SupportTicket.created_at >= cutoff_date
        ).group_by(SupportTicket.category).all()
        
        # convert to dict
        category_counts = {stat.category: stat.count for stat in stats}
        
        # get total
        total = db.query(func.count(SupportTicket.id)).filter(
            SupportTicket.created_at >= cutoff_date
        ).scalar()
        
        # get unclassified
        unclassified = db.query(func.count(SupportTicket.id)).filter(
            and_(
                SupportTicket.created_at >= cutoff_date,
                SupportTicket.category.is_(None)
            )
        ).scalar()
        
        return CategoryStats(
            technical=category_counts.get("technical", 0),
            billing=category_counts.get("billing", 0),
            general=category_counts.get("general", 0),
            total=total,
            unclassified=unclassified
        )