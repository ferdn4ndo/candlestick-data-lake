FROM python:3.9.1-alpine

WORKDIR /usr/src/app

EXPOSE 8888

RUN apk add --no-cache \
        mariadb-dev \
        build-base \
        linux-headers \
        libffi-dev

COPY ./src/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src/ .

RUN pwd
RUN ls .

CMD ["python", "main.py"]
