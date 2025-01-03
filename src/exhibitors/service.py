from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Exhibitor, ExhibitorUnverified
from .schemas import ExhibitorFullInfo, ExhibitorCreate
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
                                     Exhibitor.mail, Exhibitor.site_url, Exhibitor.description, Exhibitor.is_edited)
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
            "is_edited": exhibitor.is_edited,
            "history": history
        }

        return response

    async def get_exhibitor_by_userid(self, user_id: int, session: AsyncSession):
        statement_exhibitor = (select(Exhibitor.id, Exhibitor.exhib_name, Exhibitor.img_url, Exhibitor.tel, Exhibitor.adres,
                                     Exhibitor.mail, Exhibitor.site_url, Exhibitor.description, Exhibitor.is_edited)
                               .where(Exhibitor.user_id == user_id))
        result_exhibitor = await session.exec(statement_exhibitor)
        exhibitor = result_exhibitor.first()

        try:
            statement_history = (select(Event.date_start, Event.date_end, Event.event_name)
                                 .where(Event.id == EventExhibitor.event_id).where(EventExhibitor.exhibitor_id == exhibitor.id))
            result_history = await session.exec(statement_history)
            history = result_history.all()
        except AttributeError:
            response = {
                "exhib_name": None,
                "img_url": None,
                "tel": None,
                "adres": None,
                "mail": None,
                "site_url": None,
                "description": None,
                "is_edited": False,
                "history": None
            }
        else:
            response = {
                "exhib_name": exhibitor.exhib_name,
                "img_url": exhibitor.img_url,
                "tel": exhibitor.tel,
                "adres": exhibitor.adres,
                "mail": exhibitor.mail,
                "site_url": exhibitor.site_url,
                "description": exhibitor.description,
                "is_edited": exhibitor.is_edited,
                "history": history
            }

        return response

    async def create_exhibitor(self, exhibitor_data: ExhibitorCreate, session: AsyncSession):
        exhibitor_data_dict = exhibitor_data.model_dump()
        new_exhibitor = ExhibitorUnverified(**exhibitor_data_dict)
        session.add(new_exhibitor)
        await session.commit()

        try:
            statement = select(Exhibitor).where(Exhibitor.user_id == exhibitor_data_dict["user_id"])
            result = await session.exec(statement)
            existing_exhibitor = result.one()
        except AttributeError:
            print("No results for this user_id")
        else:
            existing_exhibitor.is_edited = True
            session.add(existing_exhibitor)
            await session.commit()
            await session.refresh(existing_exhibitor)

        return new_exhibitor

    async def update_img_url(self, user_id: int, session: AsyncSession):
        pass
