# Rest Framework
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

# External Apps
from apps.core.models import User

# Local App
from apps.travel.models import Trip
from apps.travel import views


class TestTripCRUD(APITestCase):
    """
    Test CRUD operations for trips.
    Authentication is done with client force login.
    Data used to perform tests is loaded fixture file: `initial_data.json`.

    ( GET {{apiUrl}}/api/travel/trips/ ) - List
    ( POST {{apiUrl}}/api/travel/trips/ ) - Save

    """

    fixtures = ['test_data.json']

    def setUp(self) -> None:
        # Users
        self.user = User.objects.filter(id=1).first()
        self.trip = Trip.objects.filter(id=1).first()

    def tearDown(self) -> None:
        self.user = None
        self.trip = None

    def test_trip_list(self):
        """
        Test trip list

        - Ensure passenger user can retrieve list of its trips;
        - Ensure response data has the right structure;
        - Ensure response data is expected one
        """

        factory = APIRequestFactory()
        view = views.TripView.as_view()
        request = factory.get('travel/trips/')

        force_authenticate(request, user=self.user)
        response = view(request)

        # Test a firm admin can retrieve list of households
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

        # Test response data has the expected structure
        expected_attributes = [
            'name', 'cost', 'start_date', 'end_date',
        ]

        for trip in response.data:
            for expected_attribute in expected_attributes:
                self.assertIn(expected_attribute, trip)

        # Test response data
        self.assertEqual(len(response.data), 1)
        trip = response.data[0]
        self.assertEqual(trip['name'], self.trip.name)
        self.assertEqual(trip['cost'], self.trip.cost)

    def test_trip_save_validations(self):
        """
        Test trip save validations

        - Test with None;
        - Test with missing required data;
        - Test with wrong cost value
        - Test with wrong start date < today
        """

        mock_data = [
            {
                'payload': None,
                'response': 'This field is required'
            },
            {
                'payload': {
                    "name": "Demo trip",
                    "cost": 2000
                },
                'response': 'This field is required'
            },
            {
                'payload': {
                    "name": "Demo trip",
                    "start_date": "2022-01-01",
                    "cost": "test"
                },
                'response': 'A valid number is required.'
            },
            {
                'payload': {
                    "name": "Demo trip",
                    "start_date": "2000-01-01",
                    "cost": 2000
                },
                'response': 'Trip start date must be higher or equal with current date.'
            }
        ]

        # Setup
        factory = APIRequestFactory()
        view = views.TripView.as_view()

        for data in mock_data:
            with self.subTest(data=data):
                request = factory.post(f'travel/trips/', data=data['payload'], format='json')
                force_authenticate(request, user=self.user)
                response = view(request)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(data['response'], str(response.data))
