from fastapi.templating import Jinja2Templates

import config

templates = Jinja2Templates(directory="templates")

import os
# from aiokafka import AIOKafkaProducer
import json
from typing import Any, Dict, List

from pydantic import BaseModel
# from slugify import slugify
from sqlalchemy import select, text, or_, func, update, exc, and_, insert
import shutil
# from PIL import Image

from database import async_session_maker


# Базовая функция для сбора данных с БД
async def get_data(class_, filter, is_scalar: bool = False, order_by=None):
    async with async_session_maker() as session:
        stmt = select(class_).where(filter)
        if is_scalar:
            res_query = await session.execute(stmt)
            res = res_query.scalar()
        else:
            if order_by:
                stmt = select(class_).where(filter).order_by(order_by)
            res_query = await session.execute(stmt)
            res = res_query.fetchall()
            res = [result[0] for result in res]
    return res


# async def create_upload_avatar(
#     object_id,
#     file,
#     class_,
#     path: str,
# ):
#     async with async_session_maker() as session:
#         object = await session.get(class_, object_id)
#         save_path = os.path.join(path, f"object{object.id}{file.filename}")
#
#         with open(save_path, "wb") as new_file:
#             shutil.copyfileobj(file.file, new_file)
#
#         with Image.open(save_path) as img:
#             img = img.resize((350, 350))
#             new_save_path = os.path.splitext(save_path)[0] + ".webp"
#             img.save(new_save_path, "WEBP")
#
#         # Удаляем старый файл
#         os.remove(save_path)
#
#         # Обновляем путь к файлу в объекте
#         object.pathfile = new_save_path
#         await session.commit()
#
#     return new_save_path


# async def get_images_for_objects(
#     object_ids: List[int],
#     class_: Any,
#     session: AsyncSession
# ):
#     images = []
#     for object_id in object_ids:
#         obj = await session.get(class_, object_id)
#         if not obj:
#             raise HTTPException(status_code=404, detail=f"{class_.__name__} with ID {object_id} not found")
#         images.append(await aiofiles.open(obj.pathfile, mode='rb'))  # Открываем файл в бинарном режиме и добавляем его в список
#     return images


def change_layout(text):
    conversion = {
        "q": "й",
        "w": "ц",
        "e": "у",
        "r": "к",
        "t": "е",
        "y": "н",
        "u": "г",
        "i": "ш",
        "o": "щ",
        "p": "з",
        "[": "х",
        "]": "ъ",
        "a": "ф",
        "s": "ы",
        "d": "в",
        "f": "а",
        "g": "п",
        "h": "р",
        "j": "о",
        "k": "л",
        "l": "д",
        ";": "ж",
        "'": "э",
        "z": "я",
        "x": "ч",
        "c": "с",
        "v": "м",
        "b": "и",
        "n": "т",
        "m": "ь",
        ",": "б",
        ".": "ю",
        "`": "ё",
        "й": "q",
        "ц": "w",
        "у": "e",
        "к": "r",
        "е": "t",
        "н": "y",
        "г": "u",
        "ш": "i",
        "щ": "o",
        "з": "p",
        "х": "[",
        "ъ": "]",
        "ф": "a",
        "ы": "s",
        "в": "d",
        "а": "f",
        "п": "g",
        "р": "h",
        "о": "j",
        "л": "k",
        "д": "l",
        "ж": ";",
        "э": "'",
        "я": "z",
        "ч": "x",
        "с": "c",
        "м": "v",
        "и": "b",
        "т": "n",
        "ь": "m",
        "б": ",",
        "ю": ".",
        "ё": "`",
    }

    return "".join([conversion.get(char, char) for char in text])


async def find_object(
    entity_class, entity_parameter, entity_mark: str, similarity: float = 0.3
):
    async with async_session_maker() as session:
        await session.execute(
            text(f"SET pg_trgm.similarity_threshold = {similarity};")
        )
        entity_converted = change_layout(entity_mark)
        query = select(entity_class).where(
            or_(
                func.similarity(entity_parameter, entity_mark) > 0.3,
                func.similarity(entity_parameter, entity_converted) > 0.3,
            )
        )
        result = (await session.execute(query)).unique().fetchall()

        # if entity_class != Team:
        result = [
            getattr(entity[0], entity_parameter.name) for entity in result
        ]
        # else:
        # result = [
        #     {"name": team[0].name, "slug": team[0].slug} for team in result
        # ]

        return result if result else {"result": "not found"}


async def get_object_images(
    class_: Any,
    object_ids: str,
):
    async with async_session_maker() as session:
        object_ids = object_ids.split(",")
        object_ids = list(map(lambda x: int(x), object_ids))
        images = {
            f"{(class_.__name__).lower()}{object_id}": (
                await session.get(class_, object_id)
            ).pathfile
            for object_id in object_ids
        }
        return images


async def update_object(
    data: BaseModel,
    class_,
    obj_id: int,
    attr_name: str = "name",
) -> None:
    async with async_session_maker() as session:
        update_data = {
            key: value
            for key, value in data.model_dump().items()
            if value is not None
        }
        try:
            await session.execute(
                update(class_).where(class_.id == obj_id).values(update_data)
            )
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            update_data["slug"] = f'{update_data["slug"]}-{obj_id}'
            await session.execute(
                update(class_).where(class_.id == obj_id).values(update_data)
            )
            await session.commit()


async def find_obj(class_, data: dict, options=None):
    async with async_session_maker() as session:
        query = select(class_).filter_by(**data)
        if options:
            for option in options:
                query = query.options(option)
        result = (await session.execute(query)).scalars().first()
        return result


async def insert_obj(class_, data: dict) -> int:
    async with async_session_maker() as session:
        query = insert(class_).values(data).returning(class_.id)
        result = (await session.execute(query)).scalar()
        await session.commit()
        return result
