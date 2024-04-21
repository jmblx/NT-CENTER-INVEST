#!/bin/bash


sleep 5
cd src

#gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
uvicorn main:app --host=0.0.0.0