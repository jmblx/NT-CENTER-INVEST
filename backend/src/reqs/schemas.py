from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, field_validator


class RequestRead(BaseModel):
    id: str
    user_id: UUID
    text: str

    @field_validator('id', mode="before")
    def id_to_string(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class RequestAdd(BaseModel):
    id: str
    user_id: UUID
    text: str
