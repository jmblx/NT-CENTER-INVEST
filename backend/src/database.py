# import os
#
# from beanie import init_beanie
# from motor.motor_asyncio import AsyncIOMotorClient
#
# from config import mongo_url
# from user.models import User
#
#
# class DataBase:
#     client: AsyncIOMotorClient = None
#
#     def get_db_client(self) -> AsyncIOMotorClient:
#         return self.client
#
#
# db = DataBase()
#
#
# def get_database() -> AsyncIOMotorClient:
#     return db.get_db_client()
#
#
# async def connect_to_mongo():
#     db.client = AsyncIOMotorClient(
#     mongo_url, uuidRepresentation="standard"
# )
#     await init_beanie(database=db.client.db_name, document_models=[Category, User, Event])
#
#
# def close_mongo_connection():
#     db.client.close()
import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

from config import mongo_url
from user.models import User

client = motor.motor_asyncio.AsyncIOMotorClient(
    mongo_url, uuidRepresentation="standard"
)
db = client["database_name"]


async def get_user_db():
    yield BeanieUserDatabase(User)
