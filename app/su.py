import contextlib

from db import get_async_session, get_user_db
from schemas import UserCreate
from users import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists
from settings import logging

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_superuser(email: str, password: str, is_superuser: bool = True):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser,
                            first_name="Super", last_name="User"
                        )
                    )
                    logging.info("Super User created")
    except UserAlreadyExists:
        logging.info("Super User already exists, skipping creating it...")
