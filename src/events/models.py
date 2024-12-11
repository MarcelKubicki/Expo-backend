from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, String, Double
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


class Exhibitor(SQLModel, table=True):
    __tablename__ = "exhibitor"

    id: int | None = Field(default=None, primary_key=True)
    exhib_name: str = Field(sa_column=Column(String(100)))
    img_url: str
    tel: str = Field(sa_column=Column(String(20)))
    adres: str = Field(sa_column=Column(String(100)))
    mail: str = Field(sa_column=Column(String(100)))
    site_url: str = Field(sa_column=Column(String(150)))
    description: str = Field(sa_column=Column(Text))
    category_id: int | None = Field(default=None, foreign_key="category.id")

    def __repr__(self):
        return f"<Exhibitor {self.exhib_name}>"


class EventExhibitor(SQLModel, table=True):
    __tablename__ = "event_exhibitor"

    event_id: int | None = Field(default=None, primary_key=True)
    exhibitor_id: int | None = Field(default=None, primary_key=True)
    stand_num: int

    def __repr__(self):
        return f"<EventExhibitor {self.event_id} - {self.exhibitor_id}>"
