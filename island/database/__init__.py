import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import sql
from island.core.config import DB_DSN

ASYNC_ENGINE = create_async_engine(DB_DSN, echo=True)
ASYNC_SESSION = async_sessionmaker(ASYNC_ENGINE, expire_on_commit=False)


class Base(DeclarativeBase):
    created_timestamp: Mapped[datetime.datetime] = mapped_column(
        server_default=sql.func.now()
    )
    updated_timestamp: Mapped[datetime.datetime] = mapped_column(
        server_default=sql.func.now(), onupdate=sql.func.now()
    )


async def create_all(self):
    async with ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
