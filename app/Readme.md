# TRAVELLING COMPANION API

## Requirements

It is assumed that:
-   You have Python and MySQL installed. If not, then download the latest versions from:
    * [Python](https://www.python.org/downloads/)
    * [PostgreSQL](https://www.postgresql.org/download/)

## Installation

1. **Clone git repository**:
   ```bash
   git clone https://github.com/sorin-sabo/TravellingCompanion.git
   ```

2. **Create virtual environment**
    - Windows
    ```bash
    python -m venv $(pwd)/venv
    source venv/bin/activate
    ```
   
    - OS X
    ```bash
    python3 -m venv $(pwd)/venv
    source venv/bin/activate
    ```

3. **Install requirements**:
    - Windows
    ```bash
    pip install -r requirements.txt
    ```
   
    - OS X
    ```bash
    pip3 install -r requirements.txt
    ```

4. **Change local configurations**
    - open `TravellingCompanion/settings/configurations/local_config.py`
    - create a copy of the file and name it `config.py`
    - fill in your local configurations as fallows:
        - database configuration should be your local PostgreSQL connection parameters

5. **Create local configuration file**
    - locate `TravellingCompanion/settings/environments/local.py.template`
    - make a copy of it
    - rename it to `local.py`

6. **Migrate tables with initial data included**
    ```bash 
    python manage.py migrate
    ```
7. **Populate demo data(Optional)**
   - Windows
   ```bash
   python manage.py loaddata initial_data.json
   ```
   
   - OS X
   ```bash
   python3 manage.py loaddata initial_data.json
   ```

## Run

-   Application can run directly from cmd using fallowing command:
    - Windows
    ```bash
    python manage.py runserver
    ```
      
    - OS X
    ```bash
    python3 runserver.py runserver
    ```

-   You can input a port number in case default one (8000) is used:
    ```bash
    python manage.py runserver {port_number}
    ```

-   [Endpoints](http://localhost:8000/api/)
-   [Documentation](http://localhost:8000/docs/)
-   [Administration](http://localhost:8000/admin/)

## Check

*   Since 1st Dec 2020, requirement dependency is no longer handled automatically
*   In order to check any issue run next command:
    ```bash
    python -m pip check
    ```

## Test

-   **Run all tests**:
    - PLEASE RUN ALL TESTS BEFORE EACH DEPLOY!
    - Using fallowing command:
        ```bash
        python manage.py test --verbosity 2
        ```
    - Optional `--verbosity` displays more details of test results
    - Above command will create a test database from scratch using migration scripts
    - After all tests are done test database is dropped in case `--keepdb` parameter is not added
    - In case you have a local test database change next configuration in the config.py file: 
    (`TEST_DATABASE_NAME`) and add `-k` parameter to command as fallows:
         ```bash
        python manage.py test --keepdb --verbosity 2
        ```
        - `--keepdb` is an optional parameter which tells django framework that you
        have a test database. Your local database will not be influenced by tests, but it will
        be influenced by migrations that were not yet applied on it.
       
-   **Run a specific test**:
    - Django provides a high flexibility for this purpose by adding a single parameter:
        - application name `apps.travel` or any other application:
            ```bash
            python manage.py test apps.travel --verbosity 2
            ```
        - application test `apps.travel.test_trip_view`
            ```bash
            python manage.py test apps.travel.test_trip_view --verbosity 2
            ```
-   **Always use fixtures to have test data**:
    - Fixtures can be added in test file before `setUp` function
    - To obtain a fixture Json from an application run next command:
        ```bash
        python manage.py dumpdata app_name > fixture_test_file.json
        ```

*   **Important** 
    * If a test function is not working, check renaming it to `test_{function_name}`
    * Authentication for a test can be achieved by using:
        -  `force_authenticate` & `APIRequestFactory` from django rest framework. 
        Those should be used just to test guest user authentication since other users
        can have specific rights.

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
