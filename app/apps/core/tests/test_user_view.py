# Django
from django.urls import reverse
from django.conf import settings

# Rest Framework
from rest_framework import status
from rest_framework.test import APITestCase

# Local App
from apps.core.models import User

# External App
from apps.travel.models import Passenger


# noinspection SpellCheckingInspection
class UserRegisterTest(APITestCase):
    """
    Test user register action.

    Data used to perform tests is loaded fixture file: `initial_data.json`.
    ( POST {{apiUrl}}/api/user/register/ ) - Create
    """

    fixtures = ['initial_data.json']

    def test_register_user_validations(self):
        """
        Test register user validations

        - Test with None;
        - Test with missing required data;
        - Test with wrong email address
        - Test with existing user (by email address);
        """
        # TODO: Enhance test with `parametrized` for better code quality
        test_data = [
            {
                'payload': None,
                'response': 'This field is required'
            },
            {
                'payload': {'first_name': 'Test', 'last_name': 'Register'},
                'response': 'This field is required'
            },
            {
                'payload': {
                    'first_name': 'Test',
                    'last_name': 'Register',
                    'email': 'email',
                    'password': 'Abcd1234!'
                },
                'response': 'Enter a valid email address.'
            },
            {
                'payload': {
                    'first_name': 'Test',
                    'last_name': 'Register',
                    'email': 'demo@travel.com',
                    'password': 'Abcd1234!'
                },
                'response': 'User with this email already exists.'
            }
        ]

        url = reverse('register_user')

        for data in test_data:
            response = self.client.post(url, data['payload'], format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(data['response'], str(response.data))

    def test_register_user(self):
        """
        Test register user

        - Test a user is created;
        - Test a passanger is created for related user;
        - Test user has assigned expected group
        """

        mock_data = {
            'first_name': 'Test',
            'last_name': 'Register',
            'email': 'test@travel.com',
            'password': 'Abcd1234!'
        }
        url = reverse('register_user')
        response = self.client.post(url, mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test latest added user is expected on
        user = User.objects.order_by('-id').first()
        self.assertEqual(user.email, mock_data['email'])

        # Test passanger has expected data
        passenger = Passenger.objects.filter(user_id=user.id).first()
        self.assertIsNotNone(passenger)
        self.assertEqual(passenger.first_name, mock_data['first_name'])
        self.assertEqual(passenger.last_name, mock_data['last_name'])
        self.assertEqual(passenger.email, mock_data['email'])

        # Test user has expected groups
        groups = user.groups.all()
        self.assertEqual(groups.count(), 1)
        self.assertEqual(groups[0].id, settings.PASSENGER_PERMISSION_GROUP_ID)
