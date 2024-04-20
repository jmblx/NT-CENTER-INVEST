FROM python:3.11-slim-buster

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/src

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python -m nltk.downloader punkt

RUN chmod a+x docker/*.sh
