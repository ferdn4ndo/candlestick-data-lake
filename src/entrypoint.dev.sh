#!/bin/sh

echo "Starting in DEVELOPMENT mode"

cd ..

pip install -r requirements.dev.txt

until nc -z -v -w30 db 3306
do
    echo "Waiting for database connection..."
    sleep 2
done

cd app || { echo "Unable to navigate to application folder" 1>&2; exit 1; }

alembic upgrade head

python -m tornado.autoreload main.py
