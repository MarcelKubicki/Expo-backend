from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, String, Double, Boolean
from datetime import date


class Localization(SQLModel, table=True):
    __tablename__ = "localization"

    id: int | None = Field(default=None, primary_key=True)
    loc_name: str = Field(sa_column=Column(String(60)))
    lat: float = Field(sa_column=Column(Double))
    lng: float = Field(sa_column=Column(Double))

    def __repr__(self):
        return f"<Localization {self.loc_name}>"


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: int | None = Field(default=None, primary_key=True)
    categ_name: str = Field(sa_column=Column(String(20)))
    short_categ_name: str = Field(sa_column=Column(String(60)))

    def __repr__(self):
        return f"<Category {self.categ_name}>"


class Event(SQLModel, table=True):
    __tablename__ = "event"

    id: int | None = Field(default=None, primary_key=True)
    event_name: str = Field(sa_column=Column(String(50)))
    img_url: str
    date_start: date
    date_end: date
    short_desc: str = Field(sa_column=Column(String(100)))
    long_desc: str = Field(sa_column=Column(Text))
    localization_id: int | None = Field(default=None, foreign_key="localization.id")
    category_id: int | None = Field(default=None, foreign_key="category.id")

    def __repr__(self):
        return f"<Event {self.event_name}>"


class EventExhibitor(SQLModel, table=True):
    __tablename__ = "event_exhibitor"

    id: int | None = Field(default=None, primary_key=True)
    event_id: int | None = Field(default=None, foreign_key="event.id")
    exhibitor_id: int | None = Field(default=None, foreign_key="exhibitor.id")
    stand_num: int
    is_verified: bool = Field(default=0, sa_column=Column(Boolean, default=0))

    def __repr__(self):
        return f"<EventExhibitor {self.event_id} - {self.exhibitor_id}>"


class Photo(SQLModel, table=True):
    __tablename__ = 'photo'

    id: int | None = Field(default=None, primary_key=True)
    photo_url: str
    event_id: int | None = Field(default=None, foreign_key="event.id")
