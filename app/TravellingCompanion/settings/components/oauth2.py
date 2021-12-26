import os
# -------------------------------------- OAUTH2 CONFIGURATION --------------------------------------
# Authentication domain based on external service used;
# e.g. AWS Cognito - user pool; Auth0 - https://{AUTH0_DOMAIN}
AUTH_DOMAIN = os.environ.get('AUTH_DOMAIN')
# Jwt issuer based on external service used;
# e.g. AWS Cognito - user pool; Auth0 - https://{AUTH0_DOMAIN}/
JWT_ISSUER = os.environ.get('AUTH_ISSUER')
# Jwt guest client id used for extra validation of access token
JWT_CLIENT = os.environ.get('OAUTH2_CLIENT')
# -------------------------------------- END OAUTH2 CONFIGURATION ----------------------------------
