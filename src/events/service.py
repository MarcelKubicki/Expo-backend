from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Event, Localization, Category, EventExhibitor, Photo
from .schemas import EventCreateModel, EventExhibitorVerify, JoinRequestData
from src.exhibitors.models import Exhibitor, NotificationUser


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

    async def get_upcoming_four(self, session: AsyncSession):
        statement = select(Event.id, Event.img_url).order_by(Event.date_start)
        result = await session.exec(statement)
        return result.fetchmany(4)

    async def get_event(self, session: AsyncSession, event_id: int):

        statement_exhibitors = (select(EventExhibitor.id, EventExhibitor.stand_num, EventExhibitor.is_verified, Exhibitor.exhib_name, Exhibitor.img_url, Exhibitor.tel,
                                       Exhibitor.adres, Exhibitor.mail, Exhibitor.site_url, Exhibitor.description, Exhibitor.user_id)
                                .where(EventExhibitor.exhibitor_id == Exhibitor.id)
                                .where(EventExhibitor.event_id == event_id)
                                )

        result_exhibitors = await session.exec(statement_exhibitors)
        exhibitors_list = result_exhibitors.all()

        statement_event = (select(Event.id, Event.event_name, Event.img_url, Event.date_start, Event.date_end, Event.long_desc,
                                  Localization.loc_name, Localization.lat, Localization.lng).where(Event.id == event_id)
                           .where(Event.localization_id == Localization.id))

        result_event = await session.exec(statement_event)
        event = result_event.first()

        photos_statement = select(Photo.photo_url).where(Photo.event_id == event.id)
        result_photos = await session.exec(photos_statement)
        photos = result_photos.all()

        response = {
                    "event_name": event.event_name,
                    "img_url": event.img_url,
                    "date_start": event.date_start,
                    "date_end": event.date_end,
                    "long_desc": event.long_desc,
                    "loc_name": event.loc_name,
                    "lat": event.lat,
                    "lng": event.lng,
                    "exhibitors": exhibitors_list,
                    "photos_urls": photos
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

        for photo_url in event_data_dict["photos_urls"]:
            new_photo = Photo(photo_url=photo_url, event_id=new_event.id)
            session.add(new_photo)

        await session.commit()

        return new_event

    async def accept_event_exhibitor(self, event_exhibitor_data: EventExhibitorVerify, session: AsyncSession):
        record_statement = select(EventExhibitor).where(EventExhibitor.id == event_exhibitor_data.id)
        record_result = await session.exec(record_statement)
        record = record_result.first()
        record.is_verified = True
        session.add(record)
        await session.commit()
        user_id_statement = select(Exhibitor.user_id).where(Exhibitor.id == record.exhibitor_id)
        user_id_result = await session.exec(user_id_statement)
        user_id = user_id_result.first()
        new_notification = NotificationUser(notification_id=3, user_id=user_id, message=event_exhibitor_data.message)
        session.add(new_notification)
        await session.commit()
        return {"message": "Success"}

    async def decline_event_exhibitor(self, event_exhibitor_data: EventExhibitorVerify, session: AsyncSession):
        record_statement = select(EventExhibitor).where(EventExhibitor.id == event_exhibitor_data.id)
        record_result = await session.exec(record_statement)
        record = record_result.first()
        exhibitor_id = record.exhibitor_id
        await session.delete(record)
        await session.commit()

        user_id_statement = select(Exhibitor.user_id).where(Exhibitor.id == exhibitor_id)
        user_id_result = await session.exec(user_id_statement)
        user_id = user_id_result.first()
        new_notification = NotificationUser(notification_id=4, user_id=user_id, message=event_exhibitor_data.message)
        session.add(new_notification)
        await session.commit()
        return {"message": "Decline successfully"}

    async def create_join_request(self, join_request_data: JoinRequestData, session: AsyncSession):
        join_request_data_dict = join_request_data.model_dump()
        new_record = EventExhibitor(**join_request_data_dict)
        session.add(new_record)
        await session.commit()
        return new_record
