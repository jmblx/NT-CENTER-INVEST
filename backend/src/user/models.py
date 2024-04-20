from typing import Dict, Any

from beanie import Document
from fastapi_users_db_beanie import BeanieBaseUser


class User(BeanieBaseUser, Document):
    personalization: Dict[str, Any]
