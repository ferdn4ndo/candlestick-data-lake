FROM python:3.13.0-slim

WORKDIR /usr/src

EXPOSE 8888

RUN mkdir ./app

RUN apt-get update && apt-get install -y \
        curl \
        libmariadb-dev \
        build-essential \
        linux-headers-generic \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*
COPY ./src/requirements.txt .
COPY ./src/requirements.dev.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src/entrypoint.dev.sh .
COPY ./src/entrypoint.sh .
RUN chmod +x entrypoint.dev.sh entrypoint.sh

WORKDIR /usr/src/app

ENV PYTHONPATH="/usr/src/"

HEALTHCHECK --interval=5s --timeout=5s --retries=10 --start-period=5s CMD curl -s -f http://localhost:8888/health

CMD ["/usr/src/entrypoint.sh"]
