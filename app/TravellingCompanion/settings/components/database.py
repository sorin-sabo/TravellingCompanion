import os

# ------------------------------- DATABASE CONFIGURATION -------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        'NAME':  os.environ.get("SQL_DATABASE", "db.sqlite3"),
        'USER': os.environ.get("SQL_USER", "user"),
        'PASSWORD': os.environ.get("SQL_PASSWORD", "password"),
        'HOST': os.environ.get("SQL_HOST", "localhost"),
        'PORT': os.environ.get("SQL_PORT", "5432"),
        'TEST': {
            'NAME': os.environ.get('SQL_TEST_DATABASE', 'test_db.sqlite3')
        }
    }
}

FIXTURE_DIRS = (
    'apps/core/fixtures/',
)
# ------------------------------- END DATABASE CONFIGURATION ---------------------------------------
