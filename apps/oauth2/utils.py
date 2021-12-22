# Standard Library
import base64
import json

import jwt
import requests
import six

# Django
from django.conf import settings
from django.core.cache import cache
from django.utils.functional import cached_property

# Third party Library
from jwt.algorithms import RSAAlgorithm


class TokenError(Exception):
    pass


class TokenValidator:
    """
    Class handles validation for both access and id token.
    """

    def __init__(
        self,
        jwt_auth_domain=getattr(settings, 'AUTH_DOMAIN', None),
        jwt_issuer=getattr(settings, 'JWT_ISSUER', None),
        jwt_client=getattr(settings, 'JWT_CLIENT', None),
        jwt_guest=getattr(settings, 'JWT_GUEST', None),
    ):
        """
        Token Validation

        :param str jwt_auth_domain: Authentication domain from external service
        :param str jwt_issuer: Jwt token issuer - usually same as auth domain
        :param str jwt_client: Used to validate id token client
        :param str jwt_guest: Designates if an extra validation is needed for
        guest client by providing it's id
        """

        self.jwt_auth_domain = jwt_auth_domain
        self.jwt_algorithm = getattr(settings, 'JWT_ALGORITHM', 'RS256')
        self.jwt_issuer = jwt_issuer
        self.jwt_client = jwt_client
        self.guest = jwt_guest
        # Default set to 'email'. Please check https://jwt.io when setting a different value.
        self.jwt_auth_keyword = getattr(settings, 'JWT_AUTH_FIELD', 'email')

    @cached_property
    def _json_web_keys(self):
        response = requests.get(f'{self.jwt_auth_domain}/.well-known/jwks.json')
        response.raise_for_status()
        json_data = response.json()

        return {item['kid']: json.dumps(item) for item in json_data['keys']}

    def _get_public_key(self, token=None):
        """
        Details https://jwt.io/

        :param token: Id/Access token
        :return: token public key after validation with RSAAlgorithm
        """

        try:
            headers = jwt.get_unverified_header(token)
        except jwt.DecodeError as exc:
            raise TokenError(str(exc))

        if getattr(settings, 'PUBLIC_KEYS_CACHING_ENABLED', False):
            cache_key = f'jwt:{headers["kid"]}'
            jwk_data = cache.get(cache_key)

            if not jwk_data:
                jwk_data = self._json_web_keys.get(headers['kid'])
                timeout = getattr(settings, 'PUBLIC_KEYS_CACHING_TIMEOUT', 300)
                cache.set(cache_key, jwk_data, timeout=timeout)
        else:
            jwk_data = self._json_web_keys.get(headers['kid'])

        if jwk_data:
            return RSAAlgorithm.from_jwk(jwk_data)

        return None

    def validate(self, token):
        public_key = self._get_public_key(token)

        if not public_key:
            raise TokenError("No key found for this token")

        token_type, payload = self._get_token_type(token)

        # Guest doesn't have audience under 'aud' but under 'client_id'
        audience = self.jwt_client if token_type == 'id' else None

        try:
            jwt_data = jwt.decode(
                token,
                public_key,
                audience=audience,
                issuer=self.jwt_issuer,
                algorithms=[self.jwt_algorithm],
            )
        except (jwt.InvalidTokenError, jwt.DecodeError) as exc:
            raise TokenError(str(exc))

        # Post validate audience for guest
        if token_type == 'access':
            self.validate_access_token_claims(payload)

        return jwt_data

    def validate_access_token_claims(self, token_decoded):
        if self.guest is None and 'client_id' not in token_decoded:
            # Application did not specify an audience, but
            # the token has the 'aud' claim
            raise TokenError('Invalid audience')

        audience_claims = token_decoded['client_id']

        if isinstance(audience_claims, six.string_types):
            audience_claims = [audience_claims]

        if self.guest not in audience_claims:
            raise TokenError('Invalid audience')

    def _get_token_type(self, token):
        """
        Establish token type is ID Token or Access Token.

        :return 'id' or 'access' - based on token_use received from AWS;
                token payload - token payload data decoded using base64 library;
        :rtype str, dict
        """

        token_payload_data = self._decode_token_using_base64(token)

        return token_payload_data.get('token_use', 'id'), token_payload_data

    @staticmethod
    def _decode_token_using_base64(token):
        """
        Decode token using base64 library
        :return Token decoded payload data in case decode process completes successfully
                Emtpy dictionary otherwise
        :rtype dict
        """

        if isinstance(token, six.text_type):
            token = token.encode('utf-8')

        # Decode token using base64
        try:
            signing_value, _ = token.rsplit(b'.', 1)
            _, claims_segment = signing_value.split(b'.', 1)

            rem = len(claims_segment) % 4

            if rem > 0:
                claims_segment += b'=' * (4 - rem)

            decoded_token = base64.urlsafe_b64decode(claims_segment)
            decoded_token = json.loads(decoded_token)

        except (ValueError, TypeError, AttributeError):
            decoded_token = {}

        return decoded_token
