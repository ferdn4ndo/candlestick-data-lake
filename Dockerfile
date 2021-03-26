FROM python:3.9.1-alpine

WORKDIR /usr/src

EXPOSE 8888

RUN mkdir ./app

RUN apk add --no-cache \
        mariadb-dev \
        build-base \
        linux-headers \
        libffi-dev

COPY ./src/requirements.txt .
COPY ./src/requirements.dev.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src/entrypoint.dev.sh .
COPY ./src/entrypoint.sh .
RUN chmod +x entrypoint.dev.sh entrypoint.sh

WORKDIR /usr/src/app

CMD ["entrypoint.py"]
