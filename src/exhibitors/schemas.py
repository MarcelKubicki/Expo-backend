from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import date


class Exhibitor(BaseModel):
    stand_num: int
    exhib_name: str
    img_url: HttpUrl
    tel: str
    adres: str
    mail: str
    site_url: str
    description: str


class ExhibitorListItem(BaseModel):
    id: int
    img_url: str
    exhib_name: str
    categ_name: str


class History(BaseModel):
    date_start: date
    date_end: date
    event_name: str


class ExhibitorFullInfo(BaseModel):
    exhib_name: str | None
    img_url: HttpUrl | None
    tel: str | None
    adres: str | None
    mail: str | None
    site_url: str | None
    description: str | None
    is_edited: bool | None
    history: List[History] | None


class ExhibitorCreate(BaseModel):
    exhib_name: str
    img_url: str
    adres: str
    mail: str
    site_url: str
    description: str
    user_id: int
