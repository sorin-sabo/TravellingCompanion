# ------------------------------------- DEBUG CONFIGURATION ----------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# ------------------------------------- END DEBUG CONFIGURATION ------------------------------------

# ------------------------------------- HOST CONFIGURATION -----------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'dev.travel.com'  # Replace with development host
]
# ------------------------------------- END HOST CONFIGURATION -------------------------------------

# ------------------------------------- EMAIL CONFIGURATION ----------------------------------------
SERVER_EMAIL = 'dev@travel.com'
# ------------------------------------- END EMAIL CONFIGURATION ------------------------------------

# ------------------------------------- SECURITY_MIDDLEWARE ----------------------------------------
SESSION_COOKIE_SECURE = False  # NO HTTPS
CSRF_COOKIE_SECURE = False  # NO HTTPS
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:24',
    'http://127.0.0.1:24'
]
SECURE_PROXY_SSL_HEADER = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_SSL_REDIRECT = False
SECURE_REFERRER_POLICY = 'origin'
# ------------------------------------- END SECURITY_MIDDLEWARE ------------------------------------

# ---------------------------------------- LOGGING CONFIGURATION -----------------------------------
LOGGING = {}
# -------------------------------------- END LOGGING CONFIGURATION ---------------------------------
