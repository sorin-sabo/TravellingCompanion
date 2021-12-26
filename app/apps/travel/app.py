"""
Travel API configuration
"""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TravelAppConfig(AppConfig):
    """
    Travel app config
    Used to:
        - Register Travel API as an application;
        - Rename Travel API name in Django Admin;
        - Register Travel API signals
    """

    name = 'apps.travel'
    verbose_name = _('Travel')

    # noinspection PyUnresolvedReferences
    def ready(self):
        """
        Import signals just when Django starts
        """

        # pylint: disable=import-outside-toplevel, unused-import
        import apps.travel.signals
