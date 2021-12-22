import os

# ------------------------------- DATABASE CONFIGURATION -------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOSTNAME'),
        'PORT': os.environ.get('DB_PORT'),
        'TEST': {
            'NAME': os.environ.get('TEST_DB_NAME')
        }
    }
}

FIXTURE_DIRS = (
    'apps/core/fixtures/',
)
# ------------------------------- END DATABASE CONFIGURATION ---------------------------------------
