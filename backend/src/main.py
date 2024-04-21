import os
from contextlib import asynccontextmanager

from beanie import init_beanie
# import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import db
from reference.models import Reference
from reqs.models import Request
from user.models import User
# from user.schemas import UserRead, UserCreate, UserUpdate
# from users import auth_backend, fastapi_users
from crediting.router import router as processing_credit_router
from reqs.router import router as reqs_router
import nemo.collections.asr as nemo_asr


# from config import REDIS_HOST, REDIS_PORT

@asynccontextmanager
async def lifespan(app: FastAPI):
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/stt_ru_conformer_transducer_large")
    app.state.asr_model = asr_model
    print(db.client.db_name)
    await init_beanie(
        database=db.client.name,
        document_models=[
            User,
            Request,
            Reference,
        ],
    )
    yield

app = FastAPI(lifespan=lifespan)

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

app.include_router(processing_credit_router)
app.include_router(reqs_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)



