from typing import List

from pydantic import BaseModel, ValidationError
from pymongo.errors import DuplicateKeyError

from reqs.models import Request
from utils import validate_id


class Db:

    async def add_one(self, model, data: BaseModel) -> dict:
        try:
            data = data.model_dump()
            obj = model(**data)
            if model == Request:
                if not (await validate_id(data.get("user_id"))).get("is_valid"):
                    return {"error": "category not found"}
        except DuplicateKeyError:
            return {"error": "duplicate key"}
        except ValidationError:
            return {"error": "validation error"}
        await model.insert_one(obj)
        return {"id": str(obj.id)}


    async def get_one(self, model, criteria) -> dict:
        obj = await model.find_one(criteria, fetch_links=True, nesting_depth=1)
        if not obj:
            return {"error": "not found"}
        data = dict(obj)
        return data

    async def get(self, model, criteria) -> List:
        objs = await model.find(criteria, fetch_links=True, nesting_depth=1).to_list()
        objs = [dict(obj) for obj in objs]
        return objs

    async def get_all(self, model, schema_response: BaseModel, nesting_depth=0) -> list:
        res = []

        async for obj in model.find_all(fetch_links=True, nesting_depth=nesting_depth):
            model_instance = schema_response.model_validate(obj)
            res.append(model_instance.dict(exclude_none=True))

        return res

    async def delete_one(self, model, criteria) -> dict:
        obj = await model.find_one(criteria)
        if obj:
            await obj.delete()
            return {"status": "deleted"}
        else:
            return {"error": "not found"}
