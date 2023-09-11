from typing import Optional, Union
import uuid
from datetime import datetime
from pydantic import BaseModel

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    otp_enabled: bool
    otp_verified: bool
    otp_base32: str
    otp_auth_url: str
    otp_enabled_at: Union[datetime, None]
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    otp_enabled: Optional[bool] = False
    otp_enabled: Optional[bool] = False
    otp_enabled: Optional[str] = ""
    otp_enabled: Optional[str] = ""
    otp_enabled_at: Optional[datetime] = None
    pass


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    pass


class MFAUpdate(schemas.BaseUserUpdate):
    otp_enabled: Optional[bool]
    otp_verified: Optional[bool]
    otp_base32: Optional[str]
    otp_auth_url: Optional[str]
    otp_enabled_at: Optional[datetime]
    pass


class MFAToken(BaseModel):
    token: Optional[str]
    pass


class UserDB(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    otp_enabled: Optional[bool]
    otp_verified: Optional[bool]
    otp_base32: Optional[str]
    otp_auth_url: Optional[str]
    otp_enabled_at: Optional[datetime]
    pass
