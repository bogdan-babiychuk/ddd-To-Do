

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from UrlShortner.src.db.database import init_db
from src.api.handlers import router as url_shortner_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="UrlShortner",
                  version="1.0.0",
                  description="A simple ToDo application API",
                  docs_url="/docs",
                  redoc_url="/redoc",
                  lifespan=lifespan)
    app.include_router(url_shortner_router, prefix="/url_service")
    return app

