# ------------------------------- APP CONFIGURATION ------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Admin panel
    'admin_interface',
    'colorfield',
    'django.contrib.admin',

    # Django axes - account lockout
    'axes',

    # Django ckeditor
    'ckeditor',
]

THIRD_PARTY_APPS = [
    # Rest
    'rest_framework',

    # Cognito Auth
    'drf_yasg',
]

LOCAL_APPS = [
    'apps.core',
    'apps.travel',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# ------------------------------- END APP CONFIGURATION --------------------------------------------
