from typing import Optional
import uuid

from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str
    last_name: str
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    pass


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    pass

class UserDB(schemas.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    pass
