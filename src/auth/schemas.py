from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(min_length=8, max_length=24)


class UserModel(BaseModel):
    id: int | None
    username: str
    password_hash: str = Field(exclude=True)


class UserLoginModel(BaseModel):
    username: str = Field(max_length=24)
    password: str = Field(min_length=8, max_length=24)