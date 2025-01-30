from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)
from src.settings import  DATABASE_URL
import logging
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

engine = create_async_engine(url=DATABASE_URL)
local_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession
)

# @asynccontextmanager
# async def get_session() -> AsyncSession:
#     async with local_session() as session:
#         yield session
