FROM python:3.10-slim-buster

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev

# Обновление pip и установка Cython и wheel
RUN pip install --upgrade pip setuptools wheel Cython

# Установка зависимостей из requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка Nemo Toolkit с дополнениями
RUN pip install nemo_toolkit[all]

COPY . .

# RUN python -m nltk.downloader punkt

RUN chmod a+x docker/*.sh
