from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, String, UUID, MetaData
from sqlalchemy.sql import text

from settings import DATABASE_URL

metadata = MetaData()
Base: DeclarativeMeta = declarative_base(metadata=metadata)


class User(Base, SQLAlchemyBaseUserTableUUID):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, 
                nullable=False, unique=True,
                server_default=text("gen_random_uuid()"))
    first_name: str = Column(String(length=255), nullable=False)
    last_name: str = Column(String(length=255), nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
