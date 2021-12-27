# TRAVELLING COMPANION API

## Requirements

It is assumed that:
-   You have Docker installed. If not, download the latest versions from:
    * [Docker](https://www.docker.com/products/docker-desktop)

## Installation

1. **Clone git repository**:
   ```bash
   git clone https://github.com/sorin-sabo/TravellingCompanion.git
   ```

2. **Add environment variables**
   - Create file `.env.prod` in project root directory
   - Fill in next environment variables. The ones filled in bellow can be kept,
     but the ones with no value must be filled:
    ```.dotenv
    ENV_ID=development
    SECRET_KEY=demo
    
    AUTH_DOMAIN=
    AUTH_ISSUER=
    OAUTH2_GUEST=
    OAUTH2_CLIENT=
    
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=travel_db
    SQL_USER=demo
    SQL_PASSWORD=demo
    SQL_HOST=db
    SQL_PORT=5432
    SQL_TEST_DATABASE=test_travel_db
    DATABASE=postgres
    ```
   - Create file `.env.prod.db`
   - Fill in next environment variables. The ones filled in bellow can be kept.
     Make sure that you are using same database connection parameters as above
     in case you change sample ones:
    ```.dotenv
    POSTGRES_USER=demo
    POSTGRES_PASSWORD=demo
    POSTGRES_DB=travel_db
    ```

3. **Share root directory**
    - Docker setup is made to fully support auto-reload on changes;
    - Based on docker version and OS used this operation is different:
        - Windows & OS X:
          - Docker -> Settings -> Resources -> File Sharing -> Add project root directory;
        - Linux:
          - You don't need to do anything. 
            The daemon runs natively on the Linux host and can directly access 
            the entire host filesystem with no special setup.

4. **Start image**
    ```bash
    docker-compose up -d --build
    ```

5. **Run migrations**
    ```bash
    docker-compose exec web python manage.py migrate --noinput
    ```

6. **Collect static files**
    ```bash
    docker-compose exec web python manage.py collectstatic --no-input --clear
    ```

7. **Populate demo data(Optional)**
   ```bash
   docker-compose exec web python manage.py loaddata initial_data.json
   ```

## Run

-   Upon docker run API server starts, and it's exposing:
-   [Endpoints](http://localhost:24/api/)
-   [Documentation](http://localhost:24/docs/)
-   [Administration](http://localhost:24/admin/)

## Test

-   **Run all tests**:
    - PLEASE RUN ALL TESTS BEFORE EACH DEPLOY!
    - Using fallowing command:
        ```bash
        docker-compose exec web python manage.py test --verbosity 2 --keepdb
        ```
    - Optional `--verbosity` displays more details of test results
    - Optional `--keepdb` tells django framework that you have a test database.
    - Above command will create a test database from scratch using migration scripts
    - After all tests are done test database is dropped in case `--keepdb` parameter is not added
          
-   **Run a specific test**:
    - Django provides a high flexibility for this purpose by adding a single parameter:
        - application name `apps.travel` or any other application:
            ```bash
            docker-compose exec web python manage.py test apps.travel --verbosity 2 --keepdb
            ```
        - application test `apps.travel.test_trip_view`
            ```bash
            docker-compose exec web python manage.py test apps.travel.test_trip_view --verbosity 2 --keepdb
            ```
-   **Always use fixtures to have test data**:
    - Fixtures can be added in test file before `setUp` function

*   **Important** 
    * If a test function is not working, check renaming it to `test_{function_name}`
    * Authentication for a test can be achieved by using:
        -  `force_authenticate` & `APIRequestFactory` from django rest framework. 

## Project standards

1. **Latest features**
    -   String format is done with the latest python formatters:
        ```python 
        variable_name = 'world'
        f'Hello {variable_name}!'
        ```
    -   keep libraries up to date (mostly django and DRF)

2. **Best practices**
    - use '' not "" for string formatters (not required but to keep a standard)
    - leave an empty line after docstring - `Code Readability`.
    - always specify in comments parameter type before its name - `Maintainance`
    - always give a default value to function parameters and class arguments - `Testing`
    - always store external imports in .__init__.py files - `Maintanance`
    - always inspect code before deploy and fix PEP warnings or suppress the irrelevant ones - `Code Quality`
    - do not use as line split '\'. Use () - `Code Readability and Quality` 

    - Model design standard documentation:
        * [Designing Better Models](https://simpleisbetterthancomplex.com/tips/2018/02/10/django-tip-22-designing-better-models.html)
        * [Two Scoops of Django 1.11] (Daniel Greenfeld)

3. **Code quality**
   - Pylint used to maintain code quality;
   - Rules for code quality can be consulted in `.pylintrc`
   - Current status: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`
   - Make sure before deployment that code quality is the same;
