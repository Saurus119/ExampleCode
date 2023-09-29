# KiwiTask

KiwiTask is a Flask application that utilizes the Flask web framework. It is structured with two distinct apps: one for handling API calls and another for the frontend. Each app is created as an instance of Flask. In the `app.py` file at the root directory level, we use dispatch middleware to control which requests are processed by the corresponding Flask app.

## Project Structure
  - **`Api/Config/app.py`:** The API app handles all API calls.
  - **`FrontEnd/Config/app.py`:** The frontend app provides a user interface.
  - **`Shared/`:** Includes all code that is shared between the API and FrontEnd application (Enums, DataAccessLayer, Decorators..)
  - **`Tests/`:** Implements tests for API and FrontEnd applications 

## Dispatch Middleware

In the `app.py` file, dispatch middleware is employed to route incoming requests to the appropriate Flask app based on the request path. This allows for a clean separation of concerns between the API and frontend functionality.

## API App

The API app handles all API calls and is accessible via the `/api/<route>` endpoint. The OpenAPI documentation for the API endpoints can be found at [http://127.0.0.1:5000/api/openapi.json](http://127.0.0.1:5000/api/openapi.json).
## Frontend App

The frontend app provides a user interface and is accessible at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).Frontend allows user:
- **Filtering based on "iso":**
  Apply a filter to streamline data based on the "iso" parameter.

- **Database Impact with DELETE Operation:**
  Perform a DELETE operation that directly affects the database. The operation is extended using a decorator, serving as an illustrative example.

- **Backend Check for Duplicate Countries:**
  Implement a backend check to ensure that users cannot add two identical countries. The uniqueness is determined by the combination of ISO code and country name.

- **Dynamic Page Manipulation with JavaScript:**
  Employ JavaScript to enable dynamic manipulation of data on the page without requiring full reloads. The page will only refresh during a search if the user does not provide any ISO code.

## MVP caching example
  - Post request through frontend add created country to the cached, it pair country with specific iso.
  - Delete request remove as from DB as well from cache.
  - Get in the frontend is not using cache machanism. Only for API GET cache is used.

## Getting Started

Application is wrapped into the docker containers. Dockerfile and docker-compose file are placed at the root directory of the project.

To run the application (it is expected that you have installed Docker and can run Docker commands), follow these steps:

1. Navigate into the root folder.

2. Build the Docker images:

   ```bash
   docker-compose build
   docker-compose up

## Troubleshooting and Data Modification
  If you encounter the following error during the execution of your application:
  
  `web | sqlalchemy.exc.ProgrammingError: (pyodbc.ProgrammingError) ('42S02', "[42S02] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Invalid object name 'country_detail'. (208) (SQLExecDirectW)")
  web | [SQL: SELECT country_detail.id AS country_detail_id, country_detail.iso AS country_detail_iso, country_detail.country AS country_detail_country`

## Resolution
  From witihn folder where docker files are placed run:
  - `docker exec -it <container_id> /opt/mssql-tools/bin/sqlcmd -S db -U sa -P StrongPassword!123 -d master -i /docker-entrypoint-initdb.d/migration1.sql`
  - run again docker-compose up.