from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import User

class UserService:
    async def get_user(self, username: str, session: AsyncSession):
        pass
