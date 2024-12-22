from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.events.schemas import EventCalendarItem, EventPageItem
from src.database.main import get_session
from src.events.service import EventService

event_router = APIRouter()
event_service = EventService()


@event_router.get('/', response_model=List[EventCalendarItem])
async def get_all_events(session: AsyncSession = Depends(get_session), nam: Optional[str] = None,
                         cat: Optional[str] = None, loc: Optional[str] = None, sdate: Optional[str] = None,
                         edate: Optional[str] = None):

    response = await event_service.get_all_events(session, nam, cat, loc, sdate, edate)
    return response


@event_router.get("/{event_id}", response_model=EventPageItem)
async def get_event(event_id: int, session: AsyncSession = Depends(get_session)):

    response = await event_service.get_event(session, event_id)

    return response
