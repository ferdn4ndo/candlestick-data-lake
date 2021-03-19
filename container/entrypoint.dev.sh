#!/bin/sh

pip install -r requirements.dev.txt

until nc -z -v -w30 db 3306
do
    echo "Waiting for database connection..."
    sleep 2
done

alembic upgrade head

python main.py