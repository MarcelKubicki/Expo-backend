from fastapi import FastAPI
from src.events.routes import event_router
from src.exhibitors.routes import exhibitor_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from database.main import init_db
VERSION = "v1"


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"server is starting...")
    # await init_db()
    yield
    print(f"server has been stopped")


app = FastAPI(
    title="ExpoAPI",
    description="A Rest API for expo web service",
    version=VERSION,
    lifespan=life_span
)
app.include_router(event_router, prefix=f'/api/{VERSION}/events')
app.include_router(exhibitor_router, prefix=f'/api/{VERSION}/exhibitors')

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


@app.get("/uploads/images/{file_name}")
def test_image(file_name: str):
    return FileResponse(f"uploads/images/{file_name}")
