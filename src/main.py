from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1 import (
    auth_router,
    weather_router,
    history_router,
    init_db,
    Config
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router=auth_router, prefix="/api/v1")
app.include_router(router=weather_router, prefix="/api/v1")
app.include_router(router=history_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=Config().SERVER_HOST,
        port=Config().SERVER_PORT,
        reload=False
    )
