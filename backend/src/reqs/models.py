from beanie import Document, Link
from pydantic import Field

from user.models import User


class Request(Document):
    user_id: Link[User] = Field(description="Ссылка на документ пользователя")
    text: str = Field(..., description="Текст запроса пользователя")

    class Settings:
        name = "requests"