import uuid
from typing import Optional
import json

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from db import SQLAlchemyUserDatabase

from db import User, get_user_db

import settings

from rabbit_sender import sender


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        message = {
            "type": "register",
            "email_address": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        message_json = json.dumps(message)
        await sender.send_message(message_json)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has requested for password reset.")
        #sender.send_message("reset_password", user.email, user.first_name, user.last_name, token)
        message = {
            "type": "reset_password",
            "email_address": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "token": token
        }
        message_json = json.dumps(message)
        await sender.send_message(message_json)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="/v1/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)