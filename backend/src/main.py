import os

# import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from config import REDIS_HOST, REDIS_PORT

app = FastAPI(title="requests proceed API")

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

@app.on_event("startup")
async def startup_event():
    # redis = aioredis.from_url(
    #     f"redis://{REDIS_HOST}:{REDIS_PORT}",
    #     encoding="utf8",
    #     decode_responses=True,
    # )
    pass
