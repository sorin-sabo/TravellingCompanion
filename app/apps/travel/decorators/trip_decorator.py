"""
Trip decorators

"""

# Django
from django.utils.translation import gettext_lazy as _

# Rest Framework
from rest_framework.exceptions import ParseError, NotFound

# Local App
from apps.travel.services import get_user_trip_ids


def passenger_has_access_to_trip(func):
    """
    Decorator provides extra permissions check for travel app
    """

    def wrap(obj, request, *args, **kwargs):
        """
        :param obj: Class object
        :param Request request: HTTP Request
        :param dict args: Additional arguments passed
        :param dict kwargs: Keyword arguments passed - investor id required
        :return: wrap function
        :raise: NotFound - 404 error in case trip not found in accessible trips
        :raise: ParseError - 400 error in case trip id is missing
        """

        if 'trip_id' not in kwargs:
            raise ParseError(
                _('Trip id query param is required. Please add it and try again.')
            )

        trip_ids = get_user_trip_ids(request.user)

        if kwargs['trip_id'] not in trip_ids:
            raise NotFound(_('Trip not found.'))

        return func(obj, request, *args, **kwargs)

    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__

    return wrap
