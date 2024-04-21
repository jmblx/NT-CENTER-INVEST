import os
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from config import mongo_url
from user.models import User


class DataBase:
    client: AsyncIOMotorClient = None

    def get_db_client(self) -> AsyncIOMotorClient:
        return self.client


db = DataBase()

db.client = AsyncIOMotorClient('mongodb://db:27017/mobile_helper')

async def get_user_db():
    yield BeanieUserDatabase(User)
