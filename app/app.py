from fastapi import Depends, FastAPI

from sqlalchemy import select
from rabbit_sender import sender

from db import User, get_async_session, AsyncSession
from schemas import UserCreate, UserRead, UserUpdate
from su import create_superuser
from users import auth_backend, fastapi_users

import settings

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

prefix = "/v1"
origins = ["http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/v1", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=prefix,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=prefix,
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f"{prefix}/users",
    tags=["users"],
)

@app.get("/health", tags=["healthcheck"])
async def healthcheck_route():
    return {"status": "ok"}

@app.get(f"{prefix}/users", response_model=list[UserRead], 
    dependencies=[Depends(fastapi_users.current_user(active=True, superuser=True))],
    tags=["users1"]
)
async def list_users(session: AsyncSession = Depends(get_async_session)):
    statement = select(User)
    result = await session.execute(statement)
    return result.scalars().all()

@app.on_event("startup")
async def on_startup():
    settings.configure_logging()
    settings.check_env_vars()
    await create_superuser(settings.SUPERUSER_EMAIL, settings.SUPERUSER_PASSWORD, True)
    
@app.on_event("shutdown")
async def on_shutdown():
    await sender.close()