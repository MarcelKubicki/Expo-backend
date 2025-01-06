from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Exhibitor, ExhibitorUnverified, NotificationUser
from .schemas import ExhibitorFullInfo, ExhibitorCreate, ExhibitorAdmin, ExhibitorAdmin2, ExhibitorVerify
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

    async def get_all_unverified_exhibitors(self, session: AsyncSession):
        statement = (select(ExhibitorUnverified.id, ExhibitorUnverified.exhib_name, ExhibitorUnverified.img_url, ExhibitorUnverified.tel, ExhibitorUnverified.adres,
                            ExhibitorUnverified.mail, ExhibitorUnverified.site_url, Category.short_categ_name, ExhibitorUnverified.description, ExhibitorUnverified.user_id)).where(ExhibitorUnverified.category_id == Category.id)
        result = await session.exec(statement)

        return result.all()

    async def get_exhibitor(self, exhibitor_id: int, session: AsyncSession):
        statement_exhibitor = (select(Exhibitor.id, Exhibitor.exhib_name, Exhibitor.img_url, Exhibitor.tel, Exhibitor.adres,
                                     Exhibitor.mail, Exhibitor.site_url, Exhibitor.description, Exhibitor.is_edited)
                               .where(Exhibitor.id == exhibitor_id))
        result_exhibitor = await session.exec(statement_exhibitor)
        exhibitor = result_exhibitor.first()

        statement_history = (select(Event.date_start, Event.date_end, Event.event_name)
                             .where(Event.id == EventExhibitor.event_id).where(EventExhibitor.exhibitor_id == exhibitor_id))
        result_history = await session.exec(statement_history)
        history = result_history.all()

        response = {
            "id": exhibitor_id,
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
                "id": None,
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
                "id": exhibitor.id,
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

        category_statement = select(Category.id).where(Category.short_categ_name == exhibitor_data_dict["category"])
        result = await session.exec(category_statement)
        category_id = result.one()

        new_exhibitor = ExhibitorUnverified(**exhibitor_data_dict)
        new_exhibitor.category_id = category_id
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

    # async def accept_verification(self, exhibitor_data: ExhibitorAdmin, session: AsyncSession):
    #     exhibitor_data_dict = exhibitor_data.model_dump()
    #     new_dict = {k: v for (k, v) in exhibitor_data_dict if k != "id" or k != "category"}
    #
    #     category_statement = select(Category.id).where(Category.short_categ_name == exhibitor_data.category)
    #     result = await session.exec(category_statement)
    #     category_id = result.one()
    #     new_dict["category_id"] = category_id
    #     new_dict["is_edited"] = False
    #
    #     try:
    #         statement = select(Exhibitor).where(Exhibitor.user_id == exhibitor_data.user_id)
    #         result = await session.exec(statement)
    #         existing_exhibitor = result.one()
    #     except AttributeError:
    #         new_exhib = Exhibitor(**new_dict)
    #         await session.add(new_exhib)
    #         await session.commit()
    #
    #     else:
    #         for k, v in new_dict.items():
    #             setattr(existing_exhibitor, k, v)
    #         await session.commit()
    #     finally:
    #         exhib_to_delete = self.get_unverified_exhib(exhibitor_data_dict["id"], session)
    #         await session.delete(exhib_to_delete)
    #         await session.commit()

    async def get_unverified_exhibitor(self, exhibitor_id: int, session: AsyncSession):
        statement = select(ExhibitorUnverified).where(ExhibitorUnverified.id == exhibitor_id)
        result = await session.exec(statement)
        exhibitor = result.one()
        return exhibitor if exhibitor is not None else None

    async def get_exhibitor_userid(self, user_id: int, session: AsyncSession):
        statement = select(Exhibitor).where(Exhibitor.user_id == user_id)
        result = await session.exec(statement)
        exhibitor = result.one()
        return exhibitor if exhibitor is not None else None

    async def delete_unverified_exhibitor(self, exhibitor_id: int, session: AsyncSession):
        exhibitor_to_delete = await self.get_unverified_exhibitor(exhibitor_id, session)
        if exhibitor_to_delete is not None:
            await session.delete(exhibitor_to_delete)
            await session.commit()
        else:
            return None

    async def set_is_edited_flag(self, user_id: int, flag_value: bool, session: AsyncSession):
        exhibitor = await self.get_exhibitor_userid(user_id, session)
        if exhibitor is not None:
            exhibitor.is_edited = flag_value
            session.add(exhibitor)
            await session.commit()
        else:
            return None

    async def decline_verification(self, verify_data: ExhibitorVerify, session: AsyncSession):
        await self.set_is_edited_flag(verify_data.user_id, False, session)
        await self.delete_unverified_exhibitor(verify_data.id, session)
        notification_id = 2 if verify_data.message is not None else 1
        new_notification = NotificationUser(notification_id=notification_id, user_id=verify_data.user_id,
                                            message=verify_data.message)
        session.add(new_notification)
        await session.commit()

    async def update_exhibitor(self, unverified_exhibitor_id: int, user_id: int, session: AsyncSession):
        unverified_exhibitor = await self.get_unverified_exhibitor(unverified_exhibitor_id, session)
        unverified_exhibitor_dict = unverified_exhibitor.model_dump()
        exhibitor = await self.get_exhibitor_userid(user_id, session)
        for k, v in unverified_exhibitor_dict.items():
            if k != "id":
                setattr(exhibitor, k, v)
        await session.commit()

    async def accept_verification(self, verify_data: ExhibitorVerify, session: AsyncSession):
        await self.update_exhibitor(verify_data.id, verify_data.user_id, session)
        await self.decline_verification(verify_data, session)
