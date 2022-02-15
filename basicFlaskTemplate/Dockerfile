from alpine:latest

RUN apk update

RUN apk add --no-cache python3

RUN pip3 install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN chmod +x gunicorn_starter.sh

RUN pip3 --no-cache-dir install -r requirements.txt

ENTRYPOINT ["./gunicorn_starter.sh"]
