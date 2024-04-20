from typing import Any, Dict, Optional, List

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi_users import schemas
from pydantic import field_validator

from reqs.schemas import RequestRead


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: str
    personalization: Optional[Dict[str, Any]] = {}
    requests: Optional[List[RequestRead]]

    @field_validator('id', mode="before")
    def id_to_string(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    personalization: Optional[Dict[str, Any]] = {}

    class Config:
        from_attributes = True


class UserUpdate(schemas.BaseUserUpdate):
    personalization: Optional[Dict[str, Any]] = {}

    class Config:
        from_attributes = True