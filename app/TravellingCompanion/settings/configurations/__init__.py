import os
from .local_config import config

CONFIG_LOCATION = os.path.dirname(os.path.abspath(__file__))

if os.path.isfile(f'{CONFIG_LOCATION}\config.py'):
    # noinspection PyUnresolvedReferences
    from app.TravellingCompanion.settings.configurations.config import config
