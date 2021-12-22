# ------------------------------- DRF DOCUMENTATION CONFIGURATION ----------------------------------
SWAGGER_SETTINGS = {
   'DEFAULT_AUTO_SCHEMA_CLASS': 'apps.core.services.CamelCaseOperationIDAutoSchema',
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
    'HIDE_HOSTNAME': False,
    'PATH_IN_MIDDLE': True,
    'NATIVE_SCROLLBARS': True
}
# ------------------------------- END DRF DOCUMENTATION CONFIGURATION ------------------------------
