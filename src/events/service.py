from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Event, Localization, Category, EventExhibitor
from .schemas import EventCreateModel
from src.exhibitors.models import Exhibitor


class EventService:
    async def get_all_events(self, session: AsyncSession, nam, cat, loc, sta, end):

        statement = (select(Event.id,
                            Event.event_name,
                            Event.img_url,
                            Event.date_start,
                            Event.date_end,
                            Event.short_desc,
                            Category.categ_name,
                            Localization.loc_name)
                     .where(Event.category_id == Category.id)
                     .where(Event.localization_id == Localization.id)).order_by(Event.date_start)

        if nam:
            statement = statement.filter(Event.event_name.like(f"%{nam}%"))
        if cat:
            statement = statement.where(Category.categ_name == cat)
        if loc:
            statement = statement.where(Localization.loc_name == loc)
        if sta:
            statement = statement.where(Event.date_start >= sta)
        if end:
            statement = statement.where(Event.date_end <= end)

        result = await session.exec(statement)

        return result.all()

    async def get_event(self, session: AsyncSession, event_id: int):

        statement_exhibitors = (select(EventExhibitor.stand_num, Exhibitor.exhib_name, Exhibitor.img_url, Exhibitor.tel,
                                       Exhibitor.adres, Exhibitor.mail, Exhibitor.site_url, Exhibitor.description)
                                .where(EventExhibitor.exhibitor_id == Exhibitor.id)
                                .where(EventExhibitor.event_id == event_id)
                                )

        result_exhibitors = await session.exec(statement_exhibitors)
        exhibitors_list = result_exhibitors.all()

        statement_event = (select(Event.event_name, Event.img_url, Event.date_start, Event.date_end, Event.long_desc,
                                  Localization.loc_name, Localization.lat, Localization.lng).where(Event.id == event_id)
                           .where(Event.localization_id == Localization.id))

        result_event = await session.exec(statement_event)
        event = result_event.first()

        response = {
                    "event_name": event.event_name,
                    "img_url": event.img_url,
                    "date_start": event.date_start,
                    "date_end": event.date_end,
                    "long_desc": event.long_desc,
                    "loc_name": event.loc_name,
                    "lat": event.lat,
                    "lng": event.lng,
                    "exhibitors": exhibitors_list
                    }

        return response

    async def create_event(self, event_data: EventCreateModel, session: AsyncSession):
        event_data_dict = event_data.model_dump()

        loc_statement = select(Localization.id).where(Localization.loc_name == event_data.localization)
        loc_result = await session.exec(loc_statement)
        loc_id = loc_result.first()

        cat_statement = select(Category.id).where(Category.short_categ_name == event_data.category)
        cat_result = await session.exec(cat_statement)
        cat_id = cat_result.first()

        new_event = Event(
            **event_data_dict,
            localization_id=loc_id,
            category_id=cat_id
        )
        session.add(new_event)
        await session.commit()
        return new_event
