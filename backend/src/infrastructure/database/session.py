from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# We will initialize this from config
engine = None
AsyncSessionLocal = None


def init_db(database_url: str):
    global engine, AsyncSessionLocal
    engine = create_async_engine(database_url, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def get_session_factory():
    global AsyncSessionLocal
    return AsyncSessionLocal
