from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.request_schemas import SupportRequestCreate, SupportRequestFilter
from app.schemas.response_schemas import (
    SupportTicketResponse, 
    SupportTicketList, 
    CategoryStats
)
from app.services.ticket_service import TicketService
from typing import Optional

router = APIRouter()

ticket_service = TicketService()

@router.post("/requests", response_model=SupportTicketResponse)
async def create_support_request(
    request: SupportRequestCreate,
    db: Session = Depends(get_db)
):
    # TODO: add auth check
    try:
        ticket = await ticket_service.create_ticket(db, request)
        return SupportTicketResponse.from_orm(ticket)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create request: {str(e)}"
        )

@router.get("/requests/{request_id}", response_model=SupportTicketResponse)
async def get_support_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    ticket = ticket_service.get_ticket(db, request_id)
    if not ticket:
        raise HTTPException(
            status_code=404, 
            detail="Support request not found"
        )
    return SupportTicketResponse.from_orm(ticket)

@router.get("/requests", response_model=SupportTicketList)
async def list_support_requests(
    category: Optional[str] = Query(
        None, 
        regex=r'^(technical|billing|general)$',
        description="Filter by category"
    ),
    limit: int = Query(
        50, 
        ge=1, 
        le=500,
        description="Number of items to return"
    ),
    offset: int = Query(
        0, 
        ge=0,
        description="Number of items to skip"
    ),
    db: Session = Depends(get_db)
):
    filters = SupportRequestFilter(
        category=category,
        limit=limit,
        offset=offset
    )
    
    tickets, total = ticket_service.get_tickets(db, filters)
    
    return SupportTicketList(
        items=[SupportTicketResponse.from_orm(ticket) for ticket in tickets],
        total=total,
        limit=limit,
        offset=offset
    )

@router.get("/stats", response_model=CategoryStats)
async def get_category_stats(
    days: int = Query(
        7, 
        ge=1, 
        le=365,
        description="Number of days to look back"
    ),
    db: Session = Depends(get_db)
):
    return ticket_service.get_category_stats(db, days)