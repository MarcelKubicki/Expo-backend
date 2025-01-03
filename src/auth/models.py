from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class Role(SQLModel, table=True):
    __tablename__ = "role"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(15)))

    def __repr__(self):
        return f"<Role {self.name}"


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String(24)))
    password_hash: str = Field(exclude=True)
    role_id: int | None = Field(default=1, foreign_key="role.id")

    def __repr__(self):
        return f"<User {self.username}>"
