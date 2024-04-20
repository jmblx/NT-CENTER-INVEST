from typing import Any, Dict, Optional, List

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import field_validator

from reqs.schemas import RequestRead


class UserRead(schemas.BaseUser[PydanticObjectId]):
    personalization: Optional[Dict[str, Any]] = {}
    requests: Optional[List[RequestRead]]


class UserCreate(schemas.BaseUserCreate):
    personalization: Optional[Dict[str, Any]] = {}


class UserUpdate(schemas.BaseUserUpdate):
    personalization: Optional[Dict[str, Any]] = {}