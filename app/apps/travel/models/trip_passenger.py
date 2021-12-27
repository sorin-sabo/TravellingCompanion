# Django
from django.db import models


class TripPassenger(models.Model):
    """
    Trip passenger is used to establish an M2M relationship
    between trips and passenger(s).
    """

    trip = models.ForeignKey(
        to='Trip',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    passenger = models.ForeignKey(
        to='Passenger',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    objects = models.Manager()

    class Meta:
        db_table = 'trip_passenger'
        app_label = 'travel'
