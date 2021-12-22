import os
# -------------------------------------- GENERAL CONFIGURATION -------------------------------------
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')

# Django 4 required key
SITE_ID = 1

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/checks/
SILENCED_SYSTEM_CHECKS = ['models.E007']

LOGIN_URL = '/admin/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

TABBED_ADMIN_USE_JQUERY_UI = True

CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
  'default': {
    'removePlugins': 'stylesheetparser',
    'allowedContent': True,
  },
}

# -------------------------------------- END GENERAL CONFIGURATION ---------------------------------

# -------------------------------------- STATIC FILE CONFIGURATION ---------------------------------
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = ['templates/']
# -------------------------------------- END STATIC FILE CONFIGURATION -----------------------------

# -------------------------------------- TEMPLATE CONFIGURATION ------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# -------------------------------------- END TEMPLATE CONFIGURATION --------------------------------


# -------------------------------------- MIDDLEWARE CONFIGURATION ----------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = [
    # Default Django middleware.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Django axes middleware
    'axes.middleware.AxesMiddleware',
]
# -------------------------------------- END MIDDLEWARE CONFIGURATION ------------------------------

# -------------------------------------- URL CONFIGURATION -----------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'TravellingCompanion.urls'
# -------------------------------------- END URL CONFIGURATION -------------------------------------

# -------------------------------------- CORS CONFIGURATION ----------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
# -------------------------------------- END CORS CONFIGURATION ------------------------------------

# -------------------------------------- AUTH CONFIGURATION ----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom authentication model
AUTH_USER_MODEL = 'core.User'
# --------------------------------------- END AUTH CONFIGURATION -----------------------------------

# --------------------------------------- WSGI CONFIGURATION ---------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'TravellingCompanion.wsgi.application'
# --------------------------------------- END WSGI CONFIGURATION -----------------------------------

# --------------------------------------- ADMIN SESSION CONFIGURATION ------------------------------
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_SECONDS = 3600  # 1 hour
# --------------------------------------- END ADMIN SESSION CONFIGURATION --------------------------

# --------------------------------------- PASSWORD POLICIES CONFIGURATION --------------------------
SITE_ID = 1
PASSWORD_DURATION_SECONDS = 36 * 60**3  # Require a password change each 90 days
PASSWORD_HISTORY_COUNT = 12  # A history of 12 passwords used when changing password
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
# --------------------------------------- END PASSWORD POLICIES CONFIGURATION ----------------------

# --------------------------------------- AXES USER LOCK CONFIGURATION -----------------------------
AXES_FAILURE_LIMIT = 6
AXES_COOLOFF_TIME = None
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
AXES_LOCKOUT_TEMPLATE = ''
# --------------------------------------- END AXES USER LOCK CONFIGURATION -------------------------

# --------------------------------------- SECURITY_MIDDLEWARE --------------------------------------
# Prevent browser from identifying content types incorrectly.
# Adds 'X-Content-Type-Options: nosniff' header.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Activate the browser's XSS filtering and help prevent XSS attacks.
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

# Using a secure-only session cookie makes it more difficult
# for network traffic sniffers to hijack user sessions.
SESSION_COOKIE_SECURE = True

# Using a secure-only CSRF cookie makes it more difficult
# for network traffic sniffers to steal the CSRF token.
CSRF_COOKIE_SECURE = True

SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 15768000
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'

# --------------------------------------- END SECURITY_MIDDLEWARE ----------------------------------

# --------------------------------------- EMAIL CONFIGURATION --------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
# --------------------------------------- END EMAIL CONFIGURATION ----------------------------------
