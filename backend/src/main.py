from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.infrastructure.database.session import Base, get_engine, init_db
from src.presentation.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB
    init_db(settings.database_url)
    engine = get_engine()
    # Create tables (for testing with sqlite memory, in production use Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Cleanup DB
    await engine.dispose()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
