from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from island.core.config import DB_DSN

Base = declarative_base()
ASYNC_ENGINE = create_async_engine(DB_DSN, echo=True)
ASYNC_SESSION = async_sessionmaker(
    ASYNC_ENGINE, expire_on_commit=False
)

async def create_all(self):
    async with ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)