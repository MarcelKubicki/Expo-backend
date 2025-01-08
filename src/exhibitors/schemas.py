from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import date


class Exhibitor(BaseModel):
    stand_num: int
    is_verified: bool
    id: int
    exhib_name: str
    img_url: HttpUrl
    tel: str | None
    adres: str
    mail: str
    site_url: str
    description: str
    user_id: int


class ExhibitorListItem(BaseModel):
    id: int
    img_url: str
    exhib_name: str
    categ_name: str
    short_desc: str


class History(BaseModel):
    id: int
    date_start: date
    date_end: date
    event_name: str


class ExhibitorFullInfo(BaseModel):
    id: int | None
    exhib_name: str | None
    img_url: HttpUrl | None
    tel: str | None
    adres: str | None
    mail: str | None
    site_url: str | None
    short_desc: str | None
    description: str | None
    is_edited: bool | None
    history: List[History] | None
    short_categ_name: str | None


class ExhibitorCreate(BaseModel):
    exhib_name: str
    short_desc: str | None
    img_url: str
    adres: str
    mail: str
    site_url: str
    category: str
    description: str
    user_id: int


class ExhibitorAdmin(ExhibitorCreate):
    id: int


class ExhibitorAdmin2(BaseModel):
    id: int
    exhib_name: str
    img_url: str
    adres: str
    mail: str
    site_url: str
    short_categ_name: str
    description: str
    user_id: int


class ExhibitorVerify(BaseModel):
    id: int
    user_id: int
    message: str | None


class UserNotification(BaseModel):
    id: int
    name: str
    message: str | None
