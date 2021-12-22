from os import environ

from split_settings.tools import include, optional
from .components.application import *

# Managing environment via DJANGO_ENV variable:
environ.setdefault('ENV_ID', 'production')
ENV = environ['ENV_ID']

base_settings = [
    'components/common.py',
    'components/rest_framework.py',
    'components/application.py',
    'components/database.py',
    'components/oauth2.py',
    'components/documentation.py',
    'components/logging.py',
    'components/global.py',

    # Select the right environment:
    'environments/{0}.py'.format(ENV),

    # Optionally override some settings:
    optional('environments/local.py'),
]

# Include settings:
include(*base_settings)

