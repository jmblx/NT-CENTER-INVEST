from bson import ObjectId
from bson.errors import InvalidId

from user.models import User


async def validate_id(user_id: str):
    try:
        user = await User.find_one(User.id == ObjectId(user_id))
        if not user:
            return {"is_valid": False, "error": "category not found"}
        else:
            return {"is_valid": True, "category": user}
    except InvalidId:
        return {"is_valid": False, "error": "category_id incorrect format"}

