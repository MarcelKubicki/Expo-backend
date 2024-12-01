from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user="root",
    passwd='5ZUqNgji',
    database='expo'
)

mycursor = db.cursor()

app = FastAPI()

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


@app.get('/all_events')
async def all_events():
    mycursor.execute('SELECT * FROM wydarzenie')
    response = {'data': []}
    for x in mycursor:
        response['data'].append({
            'id': x[0],
            'nazwa': x[1],
            'img_url': x[2],
            'lokalizacja': x[3]
        })
    return response

@app.get("/uploads/images/{file_name}")
def test_image(file_name: str):
    return FileResponse(f"uploads/images/{file_name}")