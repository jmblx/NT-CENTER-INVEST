from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List
from pymongo import IndexModel, ASCENDING, TEXT

class Reference(Document):
    theme: Indexed(str) = Field(description="Тема вопроса, например 'Карты'")
    keywords: List[str] = Field(..., description="Список ключевых слов, связанных с вопросом")
    question: str = Field(..., description="Текст вопроса пользователя")
    response: str = Field(..., description="Ответ на вопрос пользователя")

    class Settings:
        name = "references"
        indexes = [
            "theme",
            IndexModel([("keywords", TEXT)], name="keywords_text_index")  # Создаем текстовый индекс для поиска по ключевым словам
        ]

    class Config:
        schema_extra = {
            "example": {
                "theme": "Карты",
                "keywords": ["карта", "блокировка", "смс", "мошенничество"],
                "question": "Мне пришло СМС о блокировке карты с неизвестного номера. Что я должен делать?",
                "response": "Никогда не звоните по вопросам обслуживания карты на номера, отличные от указанных на оборотной стороне Вашей карты, не раскрывайте конфиденциальную информацию о Вас и Вашей карте кому-либо и не следуйте инструкциям сомнительных лиц."
            }
        }
