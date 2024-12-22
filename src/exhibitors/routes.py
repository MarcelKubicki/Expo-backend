from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.main import get_session
from .service import ExhibitorService
from .schemas import ExhibitorListItem, ExhibitorFullInfo

exhibitor_router = APIRouter()
exhibitor_service = ExhibitorService()


@exhibitor_router.get('/', response_model=List[ExhibitorListItem])
async def get_all_exhibitors(session: AsyncSession = Depends(get_session), nam: Optional[str] = None,
                             cat: Optional[str] = None):
    response = await exhibitor_service.get_all_exhibitors(session, nam, cat)
    return response


@exhibitor_router.get('/{exhib_id}', response_model=ExhibitorFullInfo)
async def get_exhibitor(exhib_id: int, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.get_exhibitor(exhib_id, session)
    return response
