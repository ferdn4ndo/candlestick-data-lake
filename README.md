# candlestick-data-lake
A data lake application for candlestick crawling, storage and syncronous (API) and asyncronous (WebSockets) serving

# Migrations using Alembic

After making any addition or changes to the models, run the following command to generate migrations for the changes:

(remember to navigate to `/usr/src/app` inside the docker container before running it)

```
alembic revision --autogenerate -m "Adding new model"
```

To execute the migrations, use the following command:

```
alembic upgrade head
```

