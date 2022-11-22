# copy project
# pull official base image
FROM python:3.10.2-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV CELERY_BROKER_URL=redis://redis-stack-server:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis-stack-server:6379/0
ENV ENDPOINT_CONVERTED_DB=http://34.27.167.223/api/converted
ENV BUCKET_NAME=music-converter-prueba-1
ENV GOOGLE_APPLICATION_CREDENTIALS=default
ENV DATABASE_URL=default

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . ./tasks

CMD python3 -m tasks.music_task.py