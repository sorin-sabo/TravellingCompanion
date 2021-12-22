# Django Documentation Library
from drf_yasg.utils import swagger_auto_schema

# Rest Framework
from rest_framework import generics, status

# Local App
from apps.travel.models import Trip, Passenger, TripPassenger
from apps.travel.serializers import TripListSerializer, TripSaveSerializer


class TripView(generics.ListCreateAPIView):
    """
    Trip view

    * Return list of destinations using basic format.
    * Authorization: All users including guests are authorized to get list of destinations.
    """

    def get_queryset(self):
        """
        Get trips for request user

        :return: All trips created by the request user and also, all trips user is
        a passenger of.
        """

        # Init final trip ids
        trip_ids = []

        # Get trips request user is a passenger of
        passenger = Passenger.objects.filter(
            user_id=self.request.user.id
        ).first()

        if passenger is not None:
            passenger_trips = TripPassenger.objects.filter(passenger_id=passenger.id)
            trip_ids = [trip.id for trip in passenger_trips]

        # Get trips request user created
        # (One could have removed himself but he can still manage trip)

        trips_owner = Trip.objects.filter(
            created_by=self.request.user
        )
        trip_owner_ids = [trip.id for trip in trips_owner]
        trip_ids += trip_owner_ids

        # Keep only unique records
        trip_ids = list(set(trip_ids))

        return (
            Trip
            .objects
            .filter(id__in=trip_ids)
        )

    def get_serializer_class(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return TripListSerializer

        return TripSaveSerializer

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: TripSaveSerializer,
        status.HTTP_400_BAD_REQUEST: 'Validation error',
        status.HTTP_401_UNAUTHORIZED: 'Request user is not authorized to perform this action'
    })
    def post(self, request, *args, **kwargs):
        """
        Trip create

        * Authorization: Only registered passengers can create a trip
        * Create trip in system for request user
        * Returns trip saved details including it's internal identifier
        * Raises 400 error in case trip payload is invalid
        """

        response = super().post(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        """
        Extend serializer data with audit user
        """

        passenger = Passenger.objects.filter(
            user_id=self.request.user.id
        ).first()
        passengers = [passenger.id] if passenger is not None else []
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user,
            passengers=passengers
        )
