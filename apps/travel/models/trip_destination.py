# Django
from django.db import models


class TripDestination(models.Model):
    """
    Trip destination is used to establish a M2M relationship
    between trips and their destination(s).
    """

    trip = models.ForeignKey(
        to='Trip',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    destination = models.ForeignKey(
        to='Destination',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    objects = models.Manager()

    class Meta:
        db_table = 'trip_destination'
        app_label = 'travel'
