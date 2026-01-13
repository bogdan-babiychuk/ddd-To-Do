from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.api.handlers import task
from src.infra.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="ToDo Application",
                  version="1.0.0",
                  description="A simple ToDo application API",
                  docs_url="/docs",
                  redoc_url="/redoc",
                  lifespan=lifespan)
    app.include_router(task, prefix="/items", tags=["Tasks"])
    return app

