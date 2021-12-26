# Rest Framework
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

# External App
from apps.core.models import User

# Local App
from apps.travel import views


class TestTripDestinationsCRUD(APITestCase):
    """
    Test CRUD operations for destinations.
    Authentication is done with client force login.
    Data used to perform tests is loaded fixture file: `test_data.json`.

    ( GET {{apiUrl}}/api/travel/destinations/basic/list/ ) - List

    """

    fixtures = ['test_data.json']

    def setUp(self) -> None:
        self.user = User.objects.filter(id=1).first()

    def tearDown(self) -> None:
        self.user = None

    def test_destinations_basic_list(self):
        """
        Destinations basic list

        - Ensure a passenger user can retrieve list of destinations;
        - Ensure response data has the right structure;
        - Ensure data is the expected one.
        """

        expected_data = [
            dict(label='New York', value='1'),
            dict(label='London', value='2'),
        ]

        factory = APIRequestFactory()
        view = views.DestinationBasicList.as_view()
        request = factory.get('travel/destinations/basic/list/')

        force_authenticate(request, user=self.user)
        response = view(request)

        # Test a firm admin can retrieve list of households
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

        # Test response data has the expected structure
        expected_attributes = ['label', 'value']

        for destination in response.data:
            for expected_attribute in expected_attributes:
                self.assertIn(expected_attribute, destination)

        # Test response data
        self.assertEqual(response.data, expected_data)
