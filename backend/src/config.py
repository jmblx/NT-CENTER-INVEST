import os

from dotenv import load_dotenv

# Загружаем скрытые данные из файла .env

load_dotenv()

PROJECT_DEBUG = os.environ.get("PROJECT_DEBUG")

MONGO_USERNAME = os.getenv('MONGO_USERNAME', "")
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', "")
MONGO_HOSTNAME = os.getenv('MONGO_HOSTNAME', "")
MONGO_PORT = os.getenv('MONGO_PORT', "")
MONGO_DB = os.getenv('MONGO_DB', "")

mongo_url = os.getenv(
    'MONGO_URL',
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
)

SECRET_AUTH = os.environ.get("SECRET_AUTH")
