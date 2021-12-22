# Standard Library
import uuid

# Django
from django.db import models

# External App
from apps.core.models import BaseModel


class Trip(BaseModel):
    """
    Trip created by a passenger.
    A trip must have a start date, cost and at least a passenger.
    Trip name makes it easier for an end user to make a distinction between trips.
    Each trip has an uuid to enable share external trip details with friends that
    are not using the app without sharing sensitive internal data.
    """

    # DATABASE FIELDS
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    cost = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=False,
        null=False
    )
    start_date = models.DateField(
        null=False,
        blank=False
    )
    end_date = models.DateField(
        null=True,
        blank=True
    )
    destinations = models.ManyToManyField(
        to='Destination',
        through='TripDestination',
        related_name='trip_destinations'
    )
    passengers = models.ManyToManyField(
        to='Passenger',
        through='TripPassenger',
        related_name='trip_passengers'
    )

    # MANAGERS
    objects = models.Manager()

    # META CLASS
    class Meta:
        db_table = 'trip'
        app_label = 'travel'
        verbose_name = 'Trip'

    # TO STRING METHOD
    def __str__(self):
        return str(self.name)
