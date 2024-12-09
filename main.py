from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user="root",
    passwd='',
    database='expo'
)

mycursor = db.cursor()

app = FastAPI()


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


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/events', response_model=List[EventItem])
async def events(nam: Optional[str] = None, cat: Optional[str] = None, loc: Optional[str] = None,
                 std: Optional[date] = None, end: Optional[date] = None):
    if loc:
        sql = (f"SELECT wydarzenie.id, wydarzenie.nazwa, img_url, data_rozpo, data_zakon, short_desc, l.nazwa, k.nazwa"
               f" FROM wydarzenie "
               f"INNER JOIN lokalizacja AS l ON wydarzenie.lokalizacja_id = l.id "
               f"INNER JOIN kategoria AS K ON wydarzenie.kategoria_id = k.id "
               f"WHERE l.nazwa='{loc}'")
    else:
        sql = ('SELECT wydarzenie.id, wydarzenie.nazwa, img_url, data_rozpo, data_zakon, short_desc, l.nazwa, k.nazwa '
               'FROM wydarzenie '
               'INNER JOIN lokalizacja AS l ON wydarzenie.lokalizacja_id = l.id '
               'INNER JOIN kategoria AS K ON wydarzenie.kategoria_id = k.id;')
    mycursor.execute(sql)
    response = []
    for x in mycursor:
        response.append(EventItem(id=x[0], nazwa=x[1], img_url=x[2], data_rozpo=x[3], data_zakon=x[4], opis=x[5],
                                  lokalizacja=x[6], kategoria=x[7]))
    return response

@app.get("/uploads/images/{file_name}")
def test_image(file_name: str):
    return FileResponse(f"uploads/images/{file_name}")


@app.get("/event/{id}", response_model=EventPageItem)
async def get_event(id: int):
    sql_event = (f'SELECT wyd.nazwa, img_url, data_rozpo, data_zakon, long_desc, lok.nazwa, lat, lng '
                 f'FROM wydarzenie AS wyd '
                 f'INNER JOIN lokalizacja AS lok ON wyd.lokalizacja_id = lok.id '
                 f'WHERE wyd.id={id}')
    sql_exhibitors = (f"SELECT nr_stoiska, nazwa, img_url, telefon, adres, mail, strona_url, opis "
                      f"FROM wydarzenie_wystawca "
                      f"INNER JOIN wystawca ON wydarzenie_wystawca.wystawca_id = wystawca.id "
                      f"WHERE wydarzenie_id={id}")
    mycursor.execute(sql_event)
    x = mycursor.fetchone()
    mycursor.execute(sql_exhibitors)
    exhibitors = []
    for row in mycursor:
        exhibitors.append(Exhibitor(nr_stoiska=row[0], nazwa=row[1], img_url=row[2], telefon=row[3], adres=row[4],
                                    mail=row[5], strona_url=row[6], opis=row[7]))
    response = EventPageItem(nazwa=x[0], img_url=x[1], data_rozpo=x[2], data_zakon=x[3], opis=x[4], lokalizacja=x[5],
                             lat=x[6], lng=x[7], wystawcy=exhibitors)
    return response
