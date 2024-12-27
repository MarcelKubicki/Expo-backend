from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String(24)))
    password_hash: str = Field(exclude=True)

    def __repr__(self):
        return f"<User {self.username}>"
