<p align="center">
  <img src="https://raw.githubusercontent.com/ferdn4ndo/candlestick-data-lake/main/src/app/static/icon.png" alt="CSDL Logo" width="264px">
</p>

# CandleStick-Data-Lake
A data lake application for candlestick crawling, storage and syncronous (API) and asyncronous (WebSockets) serving.


## Configuration (Environment)

To configure the container, copy the `.env.template` file to `.env` (you can use the command below). An explanation of each of the variables is also available in this section.

```
cp .env.template .env
```

Then edit the file to tweak the settings as you wish before running the container.

### Variables

* **VIRTUAL_HOST**: The virtual hostname to use if you're running the container behind a reverse proxy. (Default: `[EMPTY]`)
* **LETSENCRYPT_HOST**: The virtual hostname to use in the SSL certificate generation by [Let's Encrypt](https://letsencrypt.org/) if you're running the container behind a reverse proxy. (Default: `[EMPTY]`)
* **LETSENCRYPT_EMAIL**: The hostmaster e-mail to use in the SSL certificate generation by [Let's Encrypt](https://letsencrypt.org/) if you're running the container behind a reverse proxy. (Default: `[EMPTY]`)
* **DEVELOPMENT_MODE**: If you're running the server with debug/hot reload for developing. (Default: `0`)
* **APP_PORT**: The port that the application will use. (Default: `8888`)
* **LOG_LEVEL**: The minimum log level to output on stdout/stderr. (Default: `INFO`)
* **LOG_FORMAT**: The format of the log message header. (Default: `%(asctime)s %(levelname)s %(message)s`)
* **DATE_FORMAT**: The date format to use in the system messages. (Default: `%Y-%m-%d %H:%M:%S`)
* **TEMP_FOLDER_PATH**: The path to the temp folder used during application runtime. (Default: `/usr/src/app/temp`)
* **DATABASE_URL**: The database connection URI. (Default: `mysql+mysqldb://csdl:csdl@db:3306/csdl`)
* **BASIC_AUTH_USERNAME**: The username to use in the Basic Authentication of the API endpoints. (Default: `csdl`)
* **BASIC_AUTH_PASSWORD**: The password to use in the Basic Authentication of the API endpoints. (Default: `root`)

## How to run

To build the image:

```
# Navigate to the project folder and run
docker build -f ./Dockerfile --tag candlestick-data-lake:latest .
```

For a single container run (that will expose port `8888` by default):

```
# Assuming .env file is at the current location
docker run -d --rm -e 8888 -v ./src/app:/usr/src/app --env-file ./env "$CONTAINER_NAME":local
```

Docker-compose version (will build and run):

```
# Navigate to the project folder and:
docker compose -f docker-compose.yml up --build
```

## Endpoints

* **GET /health**: provides basic health checking, retrieving a 200 OK when up & running; This endpoint requires NO authentication;

* **GET /exchanges**: lists all the exchanges in the system; This endpoint requires Basic Authentication (credentials configured in the environment variables);

* **POST /exchanges**: creates a log entry. It will retrieve a `201 Created` status code with the created log entry in case of success, or a 4xx with the error message otherwise. This endpoint requires Basic Authentication (credentials configured in the environment variables);

    * Request body:

        * `code`: The code of the exchange to be created (must be one of: `binance`);
        * `name`: The name of the exchange to be created;

    * Response schema:

        *SAME AS IN 'GET /exchanges/{code}'*

* **GET /exchanges/{id}**: retrieves a single exchange. It will retrieve a `200 Ok` status code with the requested exchange in case of success, or a 4xx with the error message otherwise. This endpoint requires Basic Authentication (credentials configured in the environment variables);

    * Response schema:

        * `id`: The unique ID of the exchange;
        * `code`: The unique code of the exchange;
        * `name`: The name of the exchange;
        * `created_at`: The timestamp (in ISO 8601 format) when the exchange was created in the application;
        * `updated_at`: The timestamp (in ISO 8601 format) when the exchange was last updated;
        * `symbols`: The list (array) of symbols that the exchange supports;

* **POST /exchanges/{id}/setup**: fetches exchange metadata (currencies, symbols) from the client services. It will retrieve a `200 Ok` status code when the setup completes successfully, or a 4xx with the error message otherwise. This endpoint requires Basic Authentication (credentials configured in the environment variables);

    * No request body required.

    * Response body:

        * `message`: A message describing the final status of the request.

* **POST /exchanges/{id}/historical**: starts fetching historical candlesticks (until getting the whole dataset) in a background process. It will retrieve a `202 Accepted` status code to indicate the process was started successfully, or a 4xx with the error message otherwise. This endpoint requires Basic Authentication (credentials configured in the environment variables);

    * Request body:

        * `symbol`: The pair symbol to start fetching historical candlesticks from (ex: `BTCUSD`);

    * Response body:

        * `message`: A message describing the final status of the request.

* **DELETE /exchanges/{id}/historical/{symbol}**: stops fetching historical candlesticks (until getting the whole dataset) in a background process. It will retrieve a `202 Accepted` status code to indicate the process was started successfully, or a 4xx with the error message otherwise. This endpoint requires Basic Authentication (credentials configured in the environment variables);

    * No request body required.

    * Response body:

        * `message`: A message describing the final status of the request.

**IMPORTANT**: The websocket endpoints are still under design!

## Testing

To run the test suite for CI/CD pipelines, run:

```
docker exec -it csdl-app sh -c "python -m unittest"
```

**IMPORTANT**: Coverage is still a ToDo

## License

This application is distributed under the [MIT](https://github.com/ferdn4ndo/candlestick-data-lake/blob/main/LICENSE) license.

## Contributors

Any help is appreciated! Feel free to review / open an issue / fork / make a PR.
