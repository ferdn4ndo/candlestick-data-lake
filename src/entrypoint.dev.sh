#!/bin/sh

echo "Starting in DEVELOPMENT mode"

cd ..

pip install -r requirements.dev.txt

cd app || { echo "Unable to navigate to application folder" 1>&2; exit 1; }

alembic upgrade head

python \
    -m debugpy --listen 0.0.0.0:5678\
    -m tornado.autoreload \
    main.py
