FROM python:3.8.7-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow \
    && apk del build-deps

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

RUN python manage.py collectstatic --noinput

RUN adduser -D dipesh
USER dipesh