from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.events.schemas import (EventCalendarItem, EventPageItem, EventCreateModel, EventExhibitorVerify,
                                UpcomingFour, JoinRequestData)
from src.database.main import get_session
from src.events.service import EventService
from src.auth.dependencies import AccessTokenBearer, RoleChecker


event_router = APIRouter()
event_service = EventService()
acc_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['user', 'admin']))
admin_role_checker = Depends(RoleChecker('admin'))


@event_router.get('/', response_model=List[EventCalendarItem])
async def get_all_events(session: AsyncSession = Depends(get_session), nam: Optional[str] = None,
                         cat: Optional[str] = None, loc: Optional[str] = None, sdate: Optional[str] = None,
                         edate: Optional[str] = None):

    response = await event_service.get_all_events(session, nam, cat, loc, sdate, edate)
    return response


@event_router.get("/event/{event_id}", response_model=EventPageItem)
async def get_event(event_id: int, session: AsyncSession = Depends(get_session)):

    response = await event_service.get_event(session, event_id)

    return response


@event_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(event_data: EventCreateModel, session: AsyncSession = Depends(get_session)):
    new_event = await event_service.create_event(event_data, session)
    return new_event


@event_router.put('/accept_exhibitor', status_code=status.HTTP_202_ACCEPTED)
async def accept_exhibitor(event_exhibitor_data: EventExhibitorVerify, session: AsyncSession = Depends(get_session)):
    response = await event_service.accept_event_exhibitor(event_exhibitor_data, session)
    return response


@event_router.put('/decline_exhibitor', status_code=status.HTTP_202_ACCEPTED)
async def decline_exhibitor(event_exhibitor_data: EventExhibitorVerify, session: AsyncSession = Depends(get_session)):
    response = await event_service.decline_event_exhibitor(event_exhibitor_data, session)
    return response


@event_router.get('/upcoming_four', response_model=List[UpcomingFour])
async def get_upcoming_four(session: AsyncSession = Depends(get_session)):
    response = await event_service.get_upcoming_four(session)
    return response


@event_router.post('/event_join_request', status_code=status.HTTP_201_CREATED)
async def create_event_join_request(join_request_data: JoinRequestData, session: AsyncSession = Depends(get_session)):
    response = await event_service.create_join_request(join_request_data, session)
    return response
