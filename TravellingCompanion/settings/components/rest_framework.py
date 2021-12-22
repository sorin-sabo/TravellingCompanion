# ------------------------------ REST FRAMEWORK CONFIGURATION --------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.oauth2.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'apps.core.permissions.CustomDjangoModelPermission',
    ]
}
# ------------------------------ END REST FRAMEWORK CONFIGURATION ----------------------------------
