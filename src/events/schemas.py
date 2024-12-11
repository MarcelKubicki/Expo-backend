from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import List


class Exhibitor(BaseModel):
    nr_stoiska: int
    nazwa: str
    img_url: HttpUrl
    telefon: str
    adres: str
    mail: str
    strona_url: str
    opis: str


class EventItem(BaseModel):
    id: int
    nazwa: str
    img_url: HttpUrl
    data_rozpo: date
    data_zakon: date
    opis: str
    lokalizacja: str
    kategoria: str


class EventPageItem(BaseModel):
    nazwa: str
    img_url: HttpUrl
    data_rozpo: date
    data_zakon: date
    opis: str
    lokalizacja: str
    lat: float
    lng: float
    wystawcy: List[Exhibitor]
