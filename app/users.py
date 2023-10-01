import uuid
from typing import List, Optional, Union
import json

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, InvalidPasswordException, UUIDIDMixin, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from common import ErrorCode
from schemas import UserCreate
from db import SQLAlchemyUserDatabase

from db import User, get_user_db

import settings

from rabbit_sender import sender

from datetime import datetime


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def create(
         self,
         user_create: User,
         safe: bool = True,
         request: Optional[Request] = None,
     ) -> User:
        """
        Create a user in the database.

        Overload the default create method to add custom validations.
        """

        await self.validate_names(user_create.first_name, user_create.last_name)

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def validate_password(self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain email"
            )
        if not any(char in password for char in ['!', '@', '#', '$', '%', '^', '&', '*',
                                                 '(', ')', '-', '_', '+', '=', '/', '\\']):
            raise InvalidPasswordException(
                reason="Password should contain atleast 1 special character"
            )
        if not any(char.isdigit() for char in password):
            raise InvalidPasswordException(
                reason="Password should contain atleast 1 number"
            )
        if not any(char.isupper() for char in password):
            raise InvalidPasswordException(
                reason="Password should contain atleast 1 uppercase letter"
            )
        if not any(char.islower() for char in password):
            raise InvalidPasswordException(
                reason="Password should contain atleast 1 lowercase letter"
            )

    async def validate_names(self, first_name: str, last_name: str) -> None:
        if len(first_name) == 0 or len(last_name) == 0:
            raise HTTPException(status_code=400,
                                detail={
                                    "code": ErrorCode.REGISTER_INVALID_NAME,
                                    "reason": "First name and last name cannot be empty"
                                    })
        if not first_name.isalpha() or not last_name.isalpha():
            raise HTTPException(status_code=400,
                                detail={
                                    "code": ErrorCode.REGISTER_INVALID_NAME,
                                    "reason": "First name and last name shouldn't contain numbers or special characters"
                                    })

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        message = {
            "type": "welcome",
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

    async def get_profile_picture_path(
        self, user: User, request: Optional[Request] = None
    ):
        try:
            await self.get_by_email(user.email)
        except exceptions.UserNotExists:
            raise exceptions.UserNotExists()
        return user.profile_picture_path

    async def change_profile_picture_path(
        self, user: User, profile_picture_file_name: str, request: Optional[Request] = None
    ):
        try:
            await self.get_by_email(user.email)
        except exceptions.UserNotExists:
            raise exceptions.UserNotExists()
        updated_user = await self.user_db.update(user, {"profile_picture_path": profile_picture_file_name})
        return updated_user

    # async def disable_otp(
    #     self, user: User, request: Optional[Request] = None
    # ):
    #     try:
    #         await self.get_by_email(user.email)
    #     except exceptions.UserNotExists():
    #         raise exceptions.UserNotExists()
    #     updated_user = await self.user_db.update(user, {"otp_enabled": False, "otp_verified": False,
    #                                                     "otp_base32": "", "otp_auth_url": "",
    #                                                     "otp_enabled_at": None})
    #     return updated_user

    # async def generate_otp(
    #     self, user: User, request: Optional[Request] = None
    # ):
    #     try:
    #         await self.get_by_email(user.email)
    #     except exceptions.UserNotExists:
    #         raise exceptions.UserNotExists()
    #     otp_base32 = pyotp.random_base32()
    #     otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(name=user.email, issuer_name="test")
    #     updated_user = await self.user_db.update(user, {"otp_auth_url": otp_auth_url, "otp_base32": otp_base32})
    #     return updated_user

    # async def enable_otp(
    #     self, user: User, token: str, request: Optional[Request] = None
    # ):
    #     try:
    #         await self.get_by_email(user.email)
    #     except exceptions.UserNotExists:
    #         raise exceptions.UserNotExists()
    #     totp = pyotp.TOTP(user.otp_base32)
    #     print(totp.now())
    #     print(f"Token: {token}")
    #     if not totp.verify(token):
    #         raise HTTPException(status_code=400,
    #                             detail={
    #                                 "code": ErrorCode.INVALID_OTP_TOKEN,
    #                                 "reason": "Invalid OTP token"
    #                                 })
    #     updated_user = await self.user_db.update(user, {"otp_enabled": True,
    #                                                     "otp_enabled_at": datetime.now()})
    #     return updated_user

    # async def validate_otp(
    #     self, token, user: User, request: Optional[Request] = None
    # ):
    #     try:
    #         await self.get_by_email(user.email)
    #     except exceptions.UserNotExists:
    #         raise exceptions.UserNotExists()
    #     totp = pyotp.TOTP(user.otp_base32)
    #     if not totp.verify(otp=token, valid_window=1):
    #         raise HTTPException(status_code=400,
    #                             detail={
    #                                 "code": ErrorCode.INVALID_OTP_TOKEN,
    #                                 "reason": "Invalid OTP token"
    #                                 })
    #     await self.user_db.update(user, {"otp_validated_until": datetime.now() + timedelta(hours=1)})
    #     return {'otp_valid': True, 'otp_validated_until': datetime.now() + timedelta(hours=1)}


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
