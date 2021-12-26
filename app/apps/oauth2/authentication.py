# Django
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import smart_str

# Rest Framework
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header
)

# Local App
from .utils import (
    TokenValidator,
    TokenError
)

# custom user model
USER_MODEL = get_user_model()


class TokenAuthentication(BaseAuthentication):
    """
    Token authentication using OAUTH2
    - id token for full authorized users
    - access token for guest users
    """

    def __init__(self):
        """
        Init custom jwt validator with local AWS Cognito settings
        """
        self._custom_jwt_validator = TokenValidator()

        super().__init__()

    # STATIC METHODS
    @staticmethod
    def get_token(request):
        """
        Get token

        :param request: Client request to get Authorization:' header from
        :return:
            - Request's 'Authorization' Id/Access token - When correct Authorization:' header
            - None - when no 'Authorization:' header or
                     Authorization:' header different then 'Bearer ...'
            - Error - when empty 'Authorization:' header or if credentials contain spaces
        """

        authorization_header = get_authorization_header(request).split()

        if not authorization_header:
            return None

        if len(authorization_header) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')

            raise exceptions.AuthenticationFailed(msg)

        if len(authorization_header) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        token_type = authorization_header[0]
        token = authorization_header[1]

        if smart_str(token_type.lower()) != 'bearer':
            return None

        return token

    # CLASS METHODS
    def authenticate(self, request):
        """
        Entry point for Django rest framework

        :param request: Client request which contains on header token to authenticate with
        :return Logged in user / guest and token
        :raises Error for invalid / expired token
        """

        token = self.get_token(request)

        if token is None:
            return None

        # Authenticate token
        try:
            jwt_payload = self._custom_jwt_validator.validate(token)
        except TokenError:
            raise exceptions.AuthenticationFailed()

        user = USER_MODEL.objects.get_or_create_for_oauth2(jwt_payload)
        return (
            user,
            token
        )

    def authenticate_header(self, request):
        """
        Authenticate header

        :param obj request: Client request - not used but required
        :raises: 401 responses for authentication failures,
                 instead of 403 - method required by the DRF
        Details on:
        https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication.
        """

        return 'Bearer: api'
