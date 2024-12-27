from pydantic import BaseModel
from datetime import date
from typing import List
from src.exhibitors.schemas import Exhibitor


class EventCalendarItem(BaseModel):
    id: int
    event_name: str
    img_url: str
    date_start: date
    date_end: date
    short_desc: str
    categ_name: str
    loc_name: str


class EventPageItem(BaseModel):
    event_name: str
    img_url: str
    date_start: date
    date_end: date
    long_desc: str
    loc_name: str
    lat: float
    lng: float
    exhibitors: List[Exhibitor]


class EventCreateModel(BaseModel):
    event_name: str
    img_url: str
    date_start: date
    date_end: date
    short_desc: str
    long_desc: str
    localization: str
    category: str
