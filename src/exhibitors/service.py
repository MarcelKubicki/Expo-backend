from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Exhibitor
from src.events.models import Category, Event, EventExhibitor


class ExhibitorService:
    async def get_all_exhibitors(self, session: AsyncSession, nam, cat):
        statement = (select(Exhibitor.id, Exhibitor.img_url, Exhibitor.exhib_name, Category.categ_name)
                     .where(Exhibitor.category_id == Category.id))

        if nam:
            statement = statement.filter(Exhibitor.exhib_name.like(f"%{nam}%"))
        if cat:
            statement = statement.where(Category.categ_name == cat)

        result = await session.exec(statement)

        return result.all()

    async def get_exhibitor(self, exhibitor_id: int, session: AsyncSession):
        statement_exhibitor = (select(Exhibitor.exhib_name, Exhibitor.img_url, Exhibitor.tel, Exhibitor.adres,
                                     Exhibitor.mail, Exhibitor.site_url, Exhibitor.description)
                               .where(Exhibitor.id == exhibitor_id))
        result_exhibitor = await session.exec(statement_exhibitor)
        exhibitor = result_exhibitor.first()

        statement_history = (select(Event.date_start, Event.date_end, Event.event_name)
                             .where(Event.id == EventExhibitor.event_id).where(EventExhibitor.exhibitor_id == exhibitor_id))
        result_history = await session.exec(statement_history)
        history = result_history.all()

        response = {
            "exhib_name": exhibitor.exhib_name,
            "img_url": exhibitor.img_url,
            "tel": exhibitor.tel,
            "adres": exhibitor.adres,
            "mail": exhibitor.mail,
            "site_url": exhibitor.site_url,
            "description": exhibitor.description,
            "history": history
        }

        return response
