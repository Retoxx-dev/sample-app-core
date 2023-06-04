from fastapi import Depends, FastAPI

from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.su import create_superuser
from app.users import auth_backend, current_active_user, fastapi_users

import app.settings as settings

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/v1", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/v1",
    tags=["auth"],
    dependencies=[Depends(fastapi_users.current_user(active=True, superuser=True))]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/v1/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/v1/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    await create_superuser(settings.SUPERUSER_EMAIL, settings.SUPERUSER_PASSWORD, True)