api_config = {
    'SECRET_KEY': 'rnhd(zyacyoy*+1d32!i@i50_!=e6fi6d5kv^bv(qa3)&+ofo8',
    'AUTH_DOMAIN': 'https://sorin.us.auth0.com',
    'AUTH_ISSUER': 'https://sorin.us.auth0.com/',
    'OAUTH2_GUEST': 'https://sample-api-auth/',
    'OAUTH2_CLIENT': 'owLNvQENGaNVzdbrrrAMEXQXSEbqIzcU'
}

database_config = {
    'DATABASE_NAME': 'travel_db',
    'DATABASE_USER': 'postgres',
    'DATABASE_PASSWORD': 'admin',
    'DATABASE_HOST': 'localhost',
    'DATABASE_PORT': '5432',
    'TEST_DATABASE_NAME': 'test_travel_db'
}

config = {**api_config, **database_config}
