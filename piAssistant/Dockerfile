FROM python:3.11.0-alpine3.17

ENV TZ=Europe/Bucharest

RUN apk add --no-cache tzdata sshpass openssh

RUN pip install telethon

RUN mkdir /application

COPY . /application

WORKDIR /application

CMD python3 /application/piAssistant.py