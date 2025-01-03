from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from src.database.redis import is_token_in_blocklist
from src.database.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_token
from .service import UserService
from .models import User
from typing import List

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.is_token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Invalid or expired token",
                    "resolution": "Get new token"
                })

        if await is_token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Invalid or revoked token",
                    "resolution": "Get new token"
                })

        self.verify_token_data(token_data)

        return token_data

    def is_token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Provide access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Provide refresh token")


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()),
                           session: AsyncSession = Depends(get_session)):
    user_username = token_details['user']['username']
    user = await user_service.get_user_by_username(user_username, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.name in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
