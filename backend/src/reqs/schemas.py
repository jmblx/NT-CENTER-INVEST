from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel, field_validator


# class RequestRead(BaseModel):
#     id: str
#     audio_path: str
#
#     @field_validator('id', mode="before")
#     def id_to_string(cls, value):
#         if isinstance(value, ObjectId):
#             return str(value)
#         return value
#
#     class Config:
#         from_attributes = True


class RequestAdd(BaseModel):
    audio_path: str

    class Config:
        from_attributes = True
