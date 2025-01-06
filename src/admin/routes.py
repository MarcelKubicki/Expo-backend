from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.main import get_session
from .service import AdminService
from src.events.schemas import EventPageItem
from typing import List

admin_router = APIRouter()
admin_service = AdminService()


@admin_router.get('/unverified_join_requests', response_model=List[EventPageItem])
async def get_unverified_join_requests(session: AsyncSession = Depends(get_session)):
    response = await admin_service.get_unverified_join_requests(session)
    return response
