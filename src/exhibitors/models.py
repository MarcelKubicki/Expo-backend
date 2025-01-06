from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, String, Boolean


class Exhibitor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    exhib_name: str = Field(sa_column=Column(String(100)))
    img_url: str | None
    tel: str | None = Field(sa_column=Column(String(20)))
    adres: str = Field(sa_column=Column(String(100)))
    mail: str = Field(sa_column=Column(String(100)))
    site_url: str = Field(sa_column=Column(String(150)))
    description: str = Field(sa_column=Column(Text))
    is_edited: bool = Field(default=0, sa_column=Column(Boolean, default=0))
    category_id: int | None = Field(default=None, foreign_key="category.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")

    def __repr__(self):
        return f"<Exhibitor {self.exhib_name}>"


class ExhibitorUnverified(SQLModel, table=True):
    __tablename__ = "exhibitor_unverified"

    id: int | None = Field(default=None, primary_key=True)
    exhib_name: str = Field(sa_column=Column(String(100)))
    img_url: str | None
    tel: str | None = Field(sa_column=Column(String(20)))
    adres: str = Field(sa_column=Column(String(100)))
    mail: str = Field(sa_column=Column(String(100)))
    site_url: str = Field(sa_column=Column(String(150)))
    description: str = Field(sa_column=Column(Text))
    category_id: int | None = Field(default=None, foreign_key="category.id")
    user_id: int = Field(default=None, foreign_key="user.id")

    def __repr__(self):
        return f"<ExhibitorUnverified {self.exhib_name}>"


class Notification(SQLModel, table=True):
    __tablename__ = "notification"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=String(150))

    def __repr__(self):
        return f"<Notification {self.name}>"


class NotificationUser(SQLModel, table=True):
    __tablename__ = "notification_user"

    id: int | None = Field(default=None, primary_key=True)
    notification_id: int = Field(foreign_key="notification.id")
    user_id: int = Field(foreign_key="user.id")
    message: str | None = Field(default=None, sa_column=Column(String(250)))

    def __repr__(self):
        return f"<NotificationUser {self.message}>"
