import json

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from src.events.models import EventExhibitor, Category
from src.exhibitors.models import Exhibitor
from src.events.models import Event
from src.events.service import EventService

event_service = EventService()

class AdminService:
    async def get_unverified_join_requests(self, session: AsyncSession):
        statement_unverif_events = (select(EventExhibitor.event_id, func.count(EventExhibitor.event_id))
                                    .join(Event).where(EventExhibitor.is_verified == False).order_by(EventExhibitor.event_id)
                                    .group_by(EventExhibitor.event_id))
        result_exhibitors = await session.exec(statement_unverif_events)

        events_list = []
        for element in result_exhibitors:
            result = await event_service.get_event(session, element.event_id)
            events_list.append(result)
        return events_list

