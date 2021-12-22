api_config = {
    'SECRET_KEY': 'REPLACE_THIS_WITH_A_SECRET_KEY',
    'AUTH_DOMAIN': '',
    'AUTH_ISSUER': '',
    'OAUTH2_GUEST': '',
    'OAUTH2_CLIENT': ''
}

database_config = {
    'DATABASE_NAME': '',
    'DATABASE_USER': '',
    'DATABASE_PASSWORD': '',
    'DATABASE_HOST': 'localhost',
    'DATABASE_PORT': '',
    'TEST_DATABASE_NAME': ''
}

config = {**api_config, **database_config}
