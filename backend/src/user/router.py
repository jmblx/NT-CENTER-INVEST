from typing import Any, Annotated

from fastapi import APIRouter, Depends, Header

from user.models import User
from user.schemas import UserRead

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: str) -> Any:
    user = dict(await User.find_one({"username": user_id}))
    if user is None:
        return {"error": "User not found"}
    user["id"] = str(user.get("_id"))
    data = UserRead(**user)
    return data
