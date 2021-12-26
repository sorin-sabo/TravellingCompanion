# Django Documentation Library
from drf_yasg.utils import swagger_auto_schema

# Rest Framework
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError

# Local App
from apps.travel.models import Trip, Passenger
from apps.travel.serializers import (
    TripListSerializer,
    TripSaveSerializer,
    TripDetailsSerializer
)
from apps.travel.decorators import passenger_has_access_to_trip
from apps.travel.services import get_user_trips


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

        return get_user_trips(self.request.user)

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


class TripDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Trip details

    * Authorization: Only logged in passenger users can get/update/delete trips.
    * Get/Update/Delete trip by id.
    * Raises 404 error in case request trip doesn't exist or is not accessible to current user
    """

    queryset = Trip.objects.all()
    serializer_class = TripDetailsSerializer

    def get_object(self):
        return Trip.objects.get(id=self.kwargs.get('trip_id'))

    def validate_before_delete(self):
        trip = self.get_object()

        if trip.created_by.id != self.request.user.id:
            raise ValidationError('You cannot remove trip managed by different user.')

    @passenger_has_access_to_trip
    def get(self, request, *args, **kwargs):
        """
        Trip details

        * Only passenger users are authorized to get trip details.
        * Get trip by id.
        * Raises 404 error in case request trip doesn't exist or is not accessible
        """

        response = super().get(request, *args, **kwargs)
        return response

    @passenger_has_access_to_trip
    def put(self, request, *args, **kwargs):
        """
        Trip update

        * Only passenger users are authorized to update trip details.
        * Update trip by id.
        * Returns trip details updated by id
        * Raises 404 error in case request trip doesn't exist or is not accessible
        """

        response = super().put(request, *args, **kwargs)
        return response

    @passenger_has_access_to_trip
    def patch(self, request, *args, **kwargs):
        """
        Trip partial update

        * Only passenger users are authorized to partial update trip details.
        * Partially update trip by id.
        * Returns trip details updated by id
        * Raises 404 error in case request trip doesn't exist or is not accessible
        """

        response = super().patch(request, *args, **kwargs)
        return response

    @passenger_has_access_to_trip
    def delete(self, request, *args, **kwargs):
        """
        Trip delete

        * Only passenger users are authorized to partial delete trip(s).
        * Delete trip by id.
        * Returns empty response with status 204
        * Raises 400 error in case trip to be deleted is owner by a different user.
        * Raises 404 error in case request trip doesn't exist or is not accessible
        """

        self.validate_before_delete()
        response = super().delete(request, *args, **kwargs)
        return response
