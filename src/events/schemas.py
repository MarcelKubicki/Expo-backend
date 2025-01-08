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
    photos_urls: List[str]


class EventCreateModel(BaseModel):
    event_name: str
    img_url: str
    photos_urls: List[str]
    date_start: date
    date_end: date
    short_desc: str
    long_desc: str
    localization: str
    category: str


class EventExhibitorVerify(BaseModel):
    id: int
    message: str | None


class UpcomingFour(BaseModel):
    id: int
    img_url: str | None


class JoinRequestData(BaseModel):
    event_id: int
    exhibitor_id: int
    stand_num: int
