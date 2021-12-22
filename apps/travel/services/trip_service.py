from apps.travel.models import (
    Trip,
    Passenger,
    TripPassenger
)


def get_user_trips(user=None):
    """
    Get user trips

    :param User user: User to get trips for
    :return: User trips
    :rtype: QuerySet
    """

    # Init final trip ids
    trip_ids = []

    if user is None:
        return Trip.objects.none()

    # Get trips request user is a passenger of
    passenger = Passenger.objects.filter(
        user_id=user.id
    ).first()

    if passenger is not None:
        passenger_trips = TripPassenger.objects.filter(passenger_id=passenger.id)
        trip_ids = [trip.id for trip in passenger_trips]

    # Get trips request user created
    # (One could have removed himself but he can still manage trip)
    trips_owner = Trip.objects.filter(
        created_by=user
    )
    trip_owner_ids = [trip.id for trip in trips_owner]
    trip_ids += trip_owner_ids

    # Keep only unique records
    trip_ids = list(set(trip_ids))

    return (
        Trip
        .objects
        .filter(id__in=trip_ids)
        .order_by('start_date')
    )


def get_user_trip_ids(user=None):
    """
    Get user trip ids

    :param User user: User to get trips for
    :return: User trip ids
    :rtype: list[int]
    """

    trips = get_user_trips(user)
    trip_ids = [trip.id for trip in trips]

    return trip_ids
