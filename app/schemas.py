from typing import Optional
import uuid

from fastapi_users import schemas

from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    profile_picture_path: Optional[str]
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    pass


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    pass


class UserProfilePicture(BaseModel):
    profile_picture_path: str


class UserDB(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    profile_picture_path: Optional[str]
    pass
