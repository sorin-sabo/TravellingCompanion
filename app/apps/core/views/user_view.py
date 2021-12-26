# Standard Library
import json
import logging
import requests
from requests.exceptions import RequestException

# Django
from django.db import transaction
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Rest Framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# Local App
from apps.core.serializers import UserRegisterSerializer, UserBasicSerializer

# External App
from apps.travel.serializers import PassengerSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserRegister(APIView):
    """
    Orchestrate user signup
    """

    permission_classes = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        User register

        * Authorization: All guests are authorized to register in the application
        * Returns status message
        """

        # Validate request data
        self.validate_request_data()

        # Perform user signup in external app - in this case Auth0
        # In a regular case scenario this functionality resides in the UI
        self.register_user_in_external_service()

        # Register user in internal database
        user_id = self.register_user()

        # Create passenger for registered user
        self.create_passenger(user_id)

        return Response(
            _('User saved successfully.'),
            status=status.HTTP_201_CREATED
        )

    def validate_request_data(self) -> None:
        """
        Validate request data
        - validate all required fields are provided

        :raises ValidationError in case of invalid payload data
        :return None
        """

        serializer = UserRegisterSerializer(data=self.request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

    # noinspection SpellCheckingInspection
    def register_user_in_external_service(self):
        """
        Register user in third party external service (Auth0)

        :raise: RequestException in case operation is not done successfully
        :return: None
        """

        headers = {
            'Content-Type': 'application/json'
        }
        first_name = self.request.data.get('last_name')
        last_name = self.request.data.get('first_name')
        user_data = {
            'connection': 'Username-Password-Authentication',
            'client_id': settings.JWT_CLIENT,
            'email': self.request.data.get('email'),
            'password': self.request.data.get('password'),
            'username': self.request.data.get('email'),
            'given_name': first_name,
            'family_name': last_name,
            'name': f'{first_name} {last_name}'
        }
        try:
            requests.post(
                url=f'{settings.AUTH_DOMAIN}/dbconnections/signup',
                data=json.dumps(user_data),
                headers=headers
            )
        except RequestException as exc:
            logger.error('Exception occurred saving event %s', str(exc))
            raise ValidationError('Register failed. Please try again later.')

    def register_user(self):
        """
        Register user in system

        :raise: ValidationError in case of invalid user data
        :return: Registered user identifier
        :rtype: int
        """

        # Save user
        user_dict = dict(
            email=self.request.data.get('email')
        )
        serializer = UserBasicSerializer(data=user_dict)

        if serializer.is_valid():
            user = serializer.save()
        else:
            raise ValidationError(serializer.errors)

        # Assign user permissions
        user.groups.set([settings.PASSENGER_PERMISSION_GROUP_ID])

        return user.id

    def create_passenger(self, user_id):
        """
        Create passenger for registered user

        :param int user_id: Registered user internal identifier to accomplish FK relationship
        :raise: ValidationError in case payload data is invalid
        :return: None
        """

        passenger_dict = dict(
            user=user_id,
            first_name=self.request.data.get('first_name'),
            last_name=self.request.data.get('last_name'),
            email=self.request.data.get('email'),
            created_by=user_id,
            updated_by=user_id,
        )
        serializer = PassengerSerializer(data=passenger_dict)

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)
