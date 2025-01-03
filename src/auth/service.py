from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import User, Role
from .schemas import UserCreateModel
from .utils import generate_password_hash


class UserService:
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User.id, User.username, User.password_hash, Role.name).where(User.role_id == Role.id).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, username: str, session: AsyncSession):
        user = await self.get_user_by_username(username, session)
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.role_id = 1
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user
