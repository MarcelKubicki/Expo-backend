from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker
from .utils import create_access_token, decode_token, verify_password
from src.database.main import get_session
from src.database.redis import add_jti_to_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta, datetime

auth_router = APIRouter()
user_service = UserService()
admin_role_checker = RoleChecker('admin')

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    username = user_data.username
    user_exists = await user_service.user_exists(username, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this username already exists")

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    username = login_data.username
    password = login_data.password

    user = await user_service.get_user_by_username(username, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "id": str(user.id),
                    'username': user.username,
                    "role_name": user.name
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "id": str(user.id),
                    'username': user.username
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": str(user.id),
                        "username": user.username,
                        "roles": [user.name]
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )
        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(content={"message": "Logout successfully"}, status_code=status.HTTP_200_OK)


@auth_router.get('/me')
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(admin_role_checker)):
    return user
