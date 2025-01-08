from fastapi import APIRouter, Depends, File, UploadFile, status
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database.main import get_session
from .service import ExhibitorService
from .schemas import ExhibitorListItem, ExhibitorFullInfo, ExhibitorCreate, ExhibitorAdmin, ExhibitorAdmin2, ExhibitorVerify, UserNotification
from uuid import uuid4
from src.config import Config

exhibitor_router = APIRouter()
exhibitor_service = ExhibitorService()


@exhibitor_router.get('/', response_model=List[ExhibitorListItem])
async def get_all_exhibitors(session: AsyncSession = Depends(get_session), nam: Optional[str] = None,
                             cat: Optional[str] = None):
    response = await exhibitor_service.get_all_exhibitors(session, nam, cat)
    return response


@exhibitor_router.get("/unverified", response_model=List[ExhibitorAdmin2])
async def get_all_unverified_exhibitors(session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.get_all_unverified_exhibitors(session)
    return response


@exhibitor_router.get('/{exhib_id}', response_model=ExhibitorFullInfo)
async def get_exhibitor(exhib_id: int, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.get_exhibitor(exhib_id, session)
    return response


@exhibitor_router.get('/user_profile/{user_id}', response_model=ExhibitorFullInfo)
async def get_exhibitor_by_userid(user_id: int, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.get_exhibitor_by_userid(user_id, session)
    return response


@exhibitor_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_exhibitor(exhibitor_data: ExhibitorCreate, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.create_exhibitor(exhibitor_data, session)
    return response


@exhibitor_router.post('/upload_profile_img', status_code=status.HTTP_201_CREATED)
async def upload_img(file: UploadFile = File(...)):
    file.filename = f"{uuid4()}.jpg"
    content = await file.read()

    with open(f"{Config.UPLOAD_IMG_PATH}{file.filename}", mode="wb") as image:
        image.write(content)

    return {"filename": f"http://127.0.0.1:8000/uploads/images/{file.filename}"}


@exhibitor_router.post('/upload_photos', status_code=status.HTTP_201_CREATED)
async def upload_photos(files: List[UploadFile]):
    photos_names_response= {"filenames": []}
    for file in files:
        file.filename = f"{uuid4()}.jpg"
        content = await file.read()

        with open(f"{Config.UPLOAD_IMG_PATH}{file.filename}", mode="wb") as image:
            image.write(content)
        final_name = f"http://127.0.0.1:8000/uploads/images/{file.filename}"
        photos_names_response["filenames"].append(final_name)

    return photos_names_response

@exhibitor_router.post('/accept', status_code=status.HTTP_202_ACCEPTED)
async def accept_verification(verify_data: ExhibitorVerify, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.accept_verification(verify_data, session)
    return response


@exhibitor_router.post('/decline')
async def decline_verification(verify_data: ExhibitorVerify, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.decline_verification(verify_data, session)
    return response


@exhibitor_router.get('/notifications/{user_id}', response_model=List[UserNotification])
async def get_user_notifications(user_id: int, session: AsyncSession = Depends(get_session)):
    response = await exhibitor_service.get_user_notifications(user_id, session)
    return response
